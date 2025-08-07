<template>
  <div class="flex" :class="message.type === 'user' ? 'justify-end' : 'justify-start'">
    <div 
      class="max-w-[70%] flex"
      :class="message.type === 'user' ? 'flex-row-reverse' : 'flex-row'"
    >
      <!-- 头像 -->
      <div class="flex-shrink-0 mx-2">
        <div 
          class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium shadow-sm"
          :class="message.type === 'user' 
            ? 'bg-primary-600 text-white' 
            : 'bg-gray-300 text-gray-700'"
        >
          {{ message.type === 'user' ? 'U' : 'AI' }}
        </div>
      </div>

      <!-- 消息内容 -->
      <div 
        class="rounded-2xl px-4 py-3 relative shadow-sm"
        :class="message.type === 'user' 
          ? 'bg-primary-600 text-white' 
          : 'bg-white text-gray-900 border border-gray-200'"
      >
        <!-- 用户消息 -->
        <div v-if="message.type === 'user'">
          <!-- 上传的图片 -->
          <div v-if="message.imageFile" class="mb-3">
            <img
              :src="message.imageFile"
              alt="用户上传的图片"
              class="max-w-xs rounded-xl border border-gray-300 shadow-sm"
            />
          </div>
          
          <!-- 文本内容 -->
          <div class="whitespace-pre-wrap">{{ message.content }}</div>
        </div>

        <!-- AI消息 -->
        <div v-else>
          <!-- 流式输入指示器 -->
          <div v-if="message.isStreaming" class="flex items-center text-yellow-600 text-sm mb-2">
            <div class="animate-spin w-3 h-3 border border-current border-t-transparent rounded-full mr-2"></div>
            正在生成回复...
          </div>

          <!-- 错误状态 -->
          <div v-if="message.hasError" class="flex items-center text-red-500 text-sm mb-2">
            <ExclamationTriangleIcon class="w-4 h-4 mr-2" />
            生成失败
          </div>

          <!-- 处理文本内容和UML卡片的混排 -->
          <div v-if="message.content || (message.plantumlResult && message.plantumlResult.success)">
            <!-- 分离代码块前的内容、代码块和代码块后的内容 -->
            <template v-if="message.plantumlResult && message.plantumlResult.success">
              <!-- 代码块前的内容 -->
              <div v-if="getPreCodeContent(message.content)" class="whitespace-pre-wrap mb-3">
                {{ getPreCodeContent(message.content) }}
              </div>
              
              <!-- UML卡片 -->
              <div class="mb-3">
                <UMLImageCard 
                  :plantuml-result="message.plantumlResult"
                  @click="$emit('click-image-card', message)"
                />
              </div>
              
              <!-- 代码块后的内容（总结文字） -->
              <div v-if="getPostCodeContent(message.content)" class="whitespace-pre-wrap">
                {{ getPostCodeContent(message.content) }}
              </div>
            </template>
            
            <!-- 如果没有PlantUML结果，正常显示文本 -->
            <div v-else-if="message.content" class="whitespace-pre-wrap">
              {{ message.content }}
            </div>
          </div>

          <!-- 流式输入光标 -->
          <span v-if="message.isStreaming" class="inline-block w-2 h-4 bg-current animate-pulse"></span>
        </div>

        <!-- 时间戳 -->
        <div 
          class="text-xs mt-2 opacity-70"
          :class="message.type === 'user' ? 'text-right' : 'text-left'"
        >
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import UMLImageCard from './UMLImageCard.vue'

defineProps({
  message: {
    type: Object,
    required: true
  }
})

defineEmits(['click-image-card'])

function formatTime(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取代码块前的内容
function getPreCodeContent(content) {
  if (!content) return ''
  
  const codeBlockPattern = /```plantuml[\s\S]*?```/
  const match = content.match(codeBlockPattern)
  
  if (match) {
    return content.substring(0, match.index).trim()
  }
  
  return ''
}

// 获取代码块后的内容（总结文字）
function getPostCodeContent(content) {
  if (!content) return ''
  
  const codeBlockPattern = /```plantuml[\s\S]*?```/
  const match = content.match(codeBlockPattern)
  
  if (match) {
    const endIndex = match.index + match[0].length
    return content.substring(endIndex).trim()
  }
  
  return ''
}
</script> 