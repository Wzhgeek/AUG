<template>
  <div class="flex flex-col h-full bg-gray-50">
    <!-- 头部 -->
    <div class="flex-shrink-0 p-6 border-b border-gray-200 bg-white rounded-bl-2xl shadow-sm">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">
            {{ currentConversation?.title || '新对话' }}
          </h2>
          <p class="text-sm text-gray-600">
            {{ currentMessages.length }} 条消息
          </p>
        </div>
        <div class="flex items-center space-x-2">
          <div
            v-if="isLoading"
            class="flex items-center text-yellow-600 text-sm"
          >
            <div class="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-2"></div>
            正在生成...
          </div>
        </div>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="flex-1 overflow-y-auto p-4" ref="messagesContainer">
      <div class="space-y-4">
        <!-- 欢迎消息 -->
        <div v-if="currentMessages.length === 0" class="text-center py-12">
          <div class="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <CodeBracketIcon class="w-8 h-8 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">
            欢迎使用UML助手
          </h3>
          <p class="text-gray-600 max-w-md mx-auto">
            发送您的需求描述或上传图片，我将为您生成相应的UML图表
          </p>
        </div>

        <!-- 消息列表 -->
        <MessageBubble
          v-for="message in currentMessages"
          :key="message.id"
          :message="message"
          @click-image-card="selectMessageForDetail"
        />
      </div>
    </div>

    <!-- 消息输入区 -->
    <div class="flex-shrink-0 border-t border-gray-200 bg-white rounded-tl-2xl">
      <MessageInput 
        @send-message="handleSendMessage"
        :disabled="isLoading"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '../stores/chat.js'
import { CodeBracketIcon } from '@heroicons/vue/24/outline'
import MessageBubble from './MessageBubble.vue'
import MessageInput from './MessageInput.vue'

const chatStore = useChatStore()
const { 
  currentConversation, 
  currentMessages, 
  isLoading 
} = storeToRefs(chatStore)

const { sendMessage, selectMessageForDetail } = chatStore

const messagesContainer = ref(null)

// 处理发送消息
async function handleSendMessage({ content, imageFile }) {
  await sendMessage(content, imageFile)
  
  // 滚动到底部
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 监听消息变化，自动滚动到底部
watch(
  () => currentMessages.value.length,
  () => {
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    })
  }
)
</script> 