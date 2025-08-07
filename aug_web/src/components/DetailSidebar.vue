<template>
  <div class="h-full flex flex-col bg-white">
    <!-- 头部 -->
    <div class="flex-shrink-0 p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">UML详情</h3>
        <button
          @click="closeDetailSidebar"
          class="p-1 hover:bg-gray-100 rounded text-gray-600 hover:text-gray-900 transition-colors"
        >
          <XMarkIcon class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- 内容区域 -->
    <div v-if="selectedMessage?.plantumlResult" class="flex-1 flex flex-col overflow-hidden">
      <!-- 切换标签 -->
      <div class="flex-shrink-0 p-4 border-b border-gray-200">
        <div class="flex space-x-1 bg-gray-100 rounded-xl p-1">
          <button
            @click="activeTab = 'image'"
            class="flex-1 px-3 py-2 text-sm font-medium rounded-lg transition-colors"
            :class="activeTab === 'image' 
              ? 'bg-primary-600 text-white' 
              : 'text-gray-700 hover:text-gray-900 hover:bg-gray-200'"
          >
            <PhotoIcon class="w-4 h-4 inline mr-2" />
            图片
          </button>
          <button
            @click="activeTab = 'code'"
            class="flex-1 px-3 py-2 text-sm font-medium rounded-lg transition-colors"
            :class="activeTab === 'code' 
              ? 'bg-primary-600 text-white' 
              : 'text-gray-700 hover:text-gray-900 hover:bg-gray-200'"
          >
            <CodeBracketIcon class="w-4 h-4 inline mr-2" />
            代码
          </button>
        </div>
      </div>

      <!-- 图片视图 -->
      <div v-if="activeTab === 'image'" class="flex-1 overflow-auto p-4">
        <div class="space-y-4">
          <!-- 图片显示 -->
          <div class="bg-gray-900 rounded-lg p-4">
            <img
              v-if="selectedMessage.plantumlResult.image_url"
              :src="getImageUrl(selectedMessage.plantumlResult.image_url)"
              alt="UML图表"
              class="w-full h-auto rounded-lg border border-gray-600"
            />
            <div v-else class="flex items-center justify-center h-48 text-gray-400">
              <PhotoIcon class="w-12 h-12" />
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex space-x-2">
            <button
              @click="downloadImage"
              class="flex-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm font-medium transition-colors"
            >
              <ArrowDownTrayIcon class="w-4 h-4 inline mr-2" />
              下载图片
            </button>
            <button
              @click="refreshImage"
              :disabled="isGeneratingImage"
              class="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
            >
              <ArrowPathIcon class="w-4 h-4 inline mr-2" :class="{ 'animate-spin': isGeneratingImage }" />
              {{ isGeneratingImage ? '生成中...' : '刷新' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 代码视图 -->
      <div v-if="activeTab === 'code'" class="flex-1 overflow-auto p-4">
        <div class="space-y-4">
          <!-- PlantUML代码 -->
          <div class="bg-gray-900 rounded-lg">
            <div class="flex items-center justify-between p-3 border-b border-gray-700">
              <h4 class="text-sm font-medium text-white">PlantUML代码</h4>
              <button
                @click="copyCode"
                class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-gray-300 text-xs rounded transition-colors"
              >
                <DocumentDuplicateIcon class="w-3 h-3 inline mr-1" />
                复制
              </button>
            </div>
            <div class="p-4">
              <textarea
                v-model="editableCode"
                class="w-full h-64 bg-transparent text-gray-300 text-sm font-mono resize-none focus:outline-none"
                placeholder="PlantUML代码将在这里显示..."
              />
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex space-x-2">
            <button
              @click="regenerateFromCode"
              :disabled="isGeneratingImage || !editableCode.trim()"
              class="flex-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
            >
              <ArrowPathIcon class="w-4 h-4 inline mr-2" :class="{ 'animate-spin': isGeneratingImage }" />
              {{ isGeneratingImage ? '生成中...' : '重新生成' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="flex-1 flex items-center justify-center text-gray-400">
      <div class="text-center">
        <DocumentIcon class="w-12 h-12 mx-auto mb-3" />
        <p>选择一个UML图表查看详情</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '../stores/chat.js'
import {
  XMarkIcon,
  PhotoIcon,
  CodeBracketIcon,
  ArrowDownTrayIcon,
  ArrowPathIcon,
  DocumentDuplicateIcon,
  DocumentIcon
} from '@heroicons/vue/24/outline'

const chatStore = useChatStore()
const { selectedMessage, isGeneratingImage } = storeToRefs(chatStore)
const { closeDetailSidebar, regenerateImage, updateMessage } = chatStore

const activeTab = ref('image')
const editableCode = ref('')

// 监听选中的消息变化，更新可编辑代码
watch(
  () => selectedMessage.value?.plantumlResult?.plantuml_code,
  (newCode) => {
    if (newCode) {
      editableCode.value = newCode
    }
  },
  { immediate: true }
)

async function downloadImage() {
  if (selectedMessage.value?.plantumlResult?.image_url) {
    const imageUrl = getImageUrl(selectedMessage.value.plantumlResult.image_url)
    
    try {
      const response = await fetch(imageUrl)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `uml-diagram-${Date.now()}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('下载图片失败:', error)
    }
  }
}

async function refreshImage() {
  if (selectedMessage.value?.plantumlResult?.plantuml_code) {
    try {
      const result = await regenerateImage(
        selectedMessage.value.plantumlResult.plantuml_code,
        'web_user_' + Date.now()
      )
      
      if (result.success) {
        // 更新消息中的PlantUML结果
        updateMessage(selectedMessage.value.id, {
          plantumlResult: {
            ...selectedMessage.value.plantumlResult,
            image_url: result.image_url,
            image_path: result.image_path
          }
        })
      }
    } catch (error) {
      console.error('刷新图片失败:', error)
    }
  }
}

async function regenerateFromCode() {
  if (editableCode.value.trim()) {
    try {
      const result = await regenerateImage(
        editableCode.value,
        'web_user_' + Date.now()
      )
      
      if (result.success) {
        // 更新消息中的PlantUML结果
        updateMessage(selectedMessage.value.id, {
          plantumlResult: {
            ...selectedMessage.value.plantumlResult,
            plantuml_code: editableCode.value,
            image_url: result.image_url,
            image_path: result.image_path
          }
        })
      }
    } catch (error) {
      console.error('重新生成失败:', error)
    }
  }
}

async function copyCode() {
  if (editableCode.value) {
    try {
      await navigator.clipboard.writeText(editableCode.value)
      // 可以添加复制成功的提示
    } catch (error) {
      console.error('复制失败:', error)
    }
  }
}

function getImageUrl(url) {
  // 如果URL已经是完整的HTTP URL，直接返回
  if (url && url.startsWith('http')) {
    return url
  }
  // 否则添加localhost前缀（用于本地开发）
  return `http://localhost:8078${url}`
}
</script> 