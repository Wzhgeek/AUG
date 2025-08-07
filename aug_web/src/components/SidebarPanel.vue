<template>
  <div class="flex flex-col h-full">
    <!-- 头部 -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-bold text-gray-900">UML助手</h1>
        <button
          @click="createNewConversation"
          class="p-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl transition-all duration-200 hover:scale-105 active:scale-95"
          title="新建对话"
        >
          <PlusIcon class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- 对话列表 -->
    <div class="flex-1 overflow-y-auto p-2">
      <div class="space-y-2">
        <div
          v-for="conversation in conversations"
          :key="conversation.id"
          @click="selectConversation(conversation.id)"
          class="group relative p-4 rounded-xl cursor-pointer transition-all duration-200 hover:scale-[1.02]"
          :class="{
            'bg-primary-600 text-white shadow-md': conversation.id === currentConversationId,
            'bg-gray-50 hover:bg-gray-100 text-gray-800': conversation.id !== currentConversationId
          }"
        >
          <!-- 对话标题 -->
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-medium truncate">
                {{ conversation.title }}
              </h3>
              <p class="text-xs opacity-75 mt-1">
                {{ formatDate(conversation.createdAt) }}
              </p>
              <p class="text-xs opacity-60 mt-1">
                {{ conversation.messages.length }} 条消息
              </p>
            </div>
            
            <!-- 删除按钮 -->
            <button
              @click.stop="deleteConversation(conversation.id)"
              class="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500 rounded-lg transition-all duration-200 hover:scale-110"
              title="删除对话"
            >
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-if="conversations.length === 0" class="text-center py-8">
        <ChatBubbleBottomCenterTextIcon class="w-12 h-12 text-gray-500 mx-auto mb-3" />
        <p class="text-gray-500 text-sm">暂无对话历史</p>
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="p-6 border-t border-gray-200">
      <div class="text-xs text-gray-600 space-y-1">
        <div class="flex items-center">
          <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
          <span>服务正常</span>
        </div>
        <div>总对话数: {{ conversations.length }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useChatStore } from '../stores/chat.js'
import { 
  PlusIcon, 
  TrashIcon, 
  ChatBubbleBottomCenterTextIcon 
} from '@heroicons/vue/24/outline'

const chatStore = useChatStore()
const { 
  conversations, 
  currentConversationId 
} = storeToRefs(chatStore)

const { 
  createNewConversation,
  selectConversation,
  deleteConversation
} = chatStore

function formatDate(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 24 * 60 * 60 * 1000) {
    return date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    })
  } else if (diff < 7 * 24 * 60 * 60 * 1000) {
    return date.toLocaleDateString('zh-CN', {
      weekday: 'short',
      hour: '2-digit',
      minute: '2-digit'
    })
  } else {
    return date.toLocaleDateString('zh-CN', {
      month: 'short',
      day: 'numeric'
    })
  }
}
</script> 