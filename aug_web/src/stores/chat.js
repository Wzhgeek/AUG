import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8078/api/v1'

export const useChatStore = defineStore('chat', () => {
  // 状态
  const conversations = ref([])
  const currentConversationId = ref(null)
  const isLoading = ref(false)
  const isGeneratingImage = ref(false)
  const selectedMessage = ref(null)
  const showDetailSidebar = ref(false)

  // 计算属性
  const currentConversation = computed(() => {
    return conversations.value.find(conv => conv.id === currentConversationId.value)
  })

  const currentMessages = computed(() => {
    return currentConversation.value?.messages || []
  })

  // 操作方法
  function createNewConversation() {
    const newConv = {
      id: Date.now().toString(),
      title: '新对话',
      messages: [],
      createdAt: new Date().toISOString()
    }
    conversations.value.push(newConv)
    currentConversationId.value = newConv.id
    return newConv
  }

  function selectConversation(conversationId) {
    currentConversationId.value = conversationId
    showDetailSidebar.value = false
    selectedMessage.value = null
  }

  function deleteConversation(conversationId) {
    const index = conversations.value.findIndex(conv => conv.id === conversationId)
    if (index > -1) {
      conversations.value.splice(index, 1)
      if (currentConversationId.value === conversationId) {
        currentConversationId.value = conversations.value.length > 0 ? conversations.value[0].id : null
      }
    }
  }

  function addMessage(message) {
    if (!currentConversation.value) {
      createNewConversation()
    }
    
    const newMessage = {
      id: Date.now().toString() + '_' + Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toISOString(),
      ...message
    }
    
    currentConversation.value.messages.push(newMessage)
    
    console.log('Added message:', {
      id: newMessage.id,
      type: newMessage.type,
      content: newMessage.content ? newMessage.content.substring(0, 50) : '',
      isStreaming: newMessage.isStreaming
    })
    
    // 更新对话标题
    if (currentConversation.value.messages.length === 1 && message.type === 'user') {
      currentConversation.value.title = message.content.substring(0, 20) + '...'
    }
    
    return newMessage
  }

  function updateMessage(messageId, updates) {
    const message = currentMessages.value.find(msg => msg.id === messageId)
    if (message) {
      // 验证消息类型，防止错误更新
      if (message.type === 'ai' && updates.content !== undefined) {
        console.log('Updating AI message content:', messageId, 'type:', message.type)
      }
      Object.assign(message, updates)
    } else {
      console.error('Message not found for update:', messageId)
      console.log('Available message IDs:', currentMessages.value.map(m => ({ id: m.id, type: m.type })))
    }
  }

  async function sendMessage(content, imageFile = null) {
    isLoading.value = true
    
    try {
      // 添加用户消息
      const userMessage = addMessage({
        type: 'user',
        content,
        imageFile: imageFile ? URL.createObjectURL(imageFile) : null
      })
      // console.log('Created user message:', userMessage.id, userMessage.type)

      // 添加AI回复消息占位符
      const aiMessage = addMessage({
        type: 'ai',
        content: '',
        isStreaming: true
      })
      // console.log('Created AI message:', aiMessage.id, aiMessage.type)

      // 准备请求数据
      let imgUrl = ''
      if (imageFile) {
        imgUrl = await uploadImage(imageFile)
      }
      
      const requestData = {
        input: content,
        userid: 'web_user_' + Date.now(),
        img_url: imgUrl
      }

      // 发送流式请求
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })

      if (!response.ok) {
        throw new Error('API请求失败')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullResponse = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              
              if (data.chunk) {
                fullResponse += data.chunk
                // console.log('Updating AI message content:', aiMessage.id, 'Current length:', fullResponse.length)
                updateMessage(aiMessage.id, { content: fullResponse })
              }
              
              if (data.plantuml_result) {
                updateMessage(aiMessage.id, {
                  plantumlResult: data.plantuml_result
                })
              }
              
              if (data.error) {
                updateMessage(aiMessage.id, {
                  content: '抱歉，发生了错误：' + data.error,
                  hasError: true
                })
              }
            } catch (e) {
              console.error('解析流数据失败:', e)
            }
          }
        }
      }

      // 确保流式处理完成后停止loading状态
      console.log('Stream completed, updating AI message:', aiMessage.id)
      updateMessage(aiMessage.id, { isStreaming: false })
      
      // 自动保存对话到数据库
      await saveConversationToDatabase(currentConversationId.value)

    } catch (error) {
      console.error('发送消息失败:', error)
      // 确保AI消息状态正确更新
      updateMessage(aiMessage.id, {
        content: '抱歉，发生了错误，请稍后重试。',
        isStreaming: false,
        hasError: true
      })
    } finally {
      isLoading.value = false
    }
  }

  async function uploadImage(file) {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      // 上传图片到服务器
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error('图片上传失败')
      }
      
      const result = await response.json()
      return result.image_url  // 现在返回的是完整的公网URL
    } catch (error) {
      console.error('图片上传失败:', error)
      // 如果上传失败，暂时使用本地URL
      return URL.createObjectURL(file)
    }
  }

  async function regenerateImage(plantumlCode, userid) {
    isGeneratingImage.value = true
    
    try {
      const response = await axios.post(`${API_BASE_URL}/plantuml/convert`, {
        plantuml_code: plantumlCode,
        userid: userid
      })
      
      return response.data
    } catch (error) {
      console.error('重新生成图片失败:', error)
      throw error
    } finally {
      isGeneratingImage.value = false
    }
  }

  function selectMessageForDetail(message) {
    selectedMessage.value = message
    showDetailSidebar.value = true
  }

  function closeDetailSidebar() {
    showDetailSidebar.value = false
    selectedMessage.value = null
  }

  // 保存对话到数据库
  async function saveConversationToDatabase(conversationId) {
    try {
      const conversation = conversations.value.find(conv => conv.id === conversationId)
      if (!conversation) return

      const response = await fetch(`${API_BASE_URL}/conversations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversation.id,
          title: conversation.title,
          messages: conversation.messages
        })
      })

      if (!response.ok) {
        console.error('保存对话失败')
      }
    } catch (error) {
      console.error('保存对话到数据库失败:', error)
    }
  }

  // 从数据库加载对话历史
  async function loadConversationsFromDatabase() {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations`)
      if (!response.ok) {
        console.error('加载对话历史失败')
        return
      }

      const savedConversations = await response.json()
      if (savedConversations && savedConversations.length > 0) {
        conversations.value = savedConversations
        if (!currentConversationId.value && conversations.value.length > 0) {
          currentConversationId.value = conversations.value[0].id
        }
      }
    } catch (error) {
      console.error('从数据库加载对话失败:', error)
    }
  }

  // 初始化时从数据库加载对话，如果没有则创建默认对话
  async function initializeConversations() {
    await loadConversationsFromDatabase()
    if (conversations.value.length === 0) {
      createNewConversation()
    }
  }

  // 初始化对话
  initializeConversations()

  return {
    // 状态
    conversations,
    currentConversationId,
    currentConversation,
    currentMessages,
    isLoading,
    isGeneratingImage,
    selectedMessage,
    showDetailSidebar,
    
    // 方法
    createNewConversation,
    selectConversation,
    deleteConversation,
    addMessage,
    updateMessage,
    sendMessage,
    regenerateImage,
    selectMessageForDetail,
    closeDetailSidebar,
    saveConversationToDatabase,
    loadConversationsFromDatabase
  }
}) 