<template>
  <div class="p-6 bg-white rounded-t-2xl">
    <!-- 图片预览 -->
    <div v-if="selectedImage" class="mb-4">
      <div class="relative inline-block">
        <img
          :src="selectedImage"
          alt="预览图片"
          class="max-w-xs max-h-32 rounded-xl border border-gray-300 shadow-sm"
        />
        <button
          @click="removeImage"
          class="absolute -top-2 -right-2 w-6 h-6 bg-red-600 hover:bg-red-700 text-white rounded-full flex items-center justify-center text-sm transition-all duration-200 hover:scale-110"
        >
          ×
        </button>
      </div>
    </div>

    <!-- 输入框区域 -->
    <div class="bg-gray-50 rounded-2xl p-4 border border-gray-200">
      <div class="flex items-end space-x-3">
        <!-- 图片上传按钮 -->
        <div class="flex-shrink-0 self-end">
          <label
            for="image-upload"
            class="inline-flex items-center justify-center w-12 h-12 bg-white hover:bg-gray-100 text-gray-600 rounded-xl cursor-pointer transition-all duration-200 hover:scale-105 shadow-sm border border-gray-200"
            title="上传图片"
          >
            <PhotoIcon class="w-5 h-5" />
            <input
              id="image-upload"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleImageSelect"
              :disabled="disabled"
            />
          </label>
        </div>

        <!-- 文本输入框 -->
        <div class="flex-1">
          <textarea
            v-model="inputText"
            ref="textareaRef"
            placeholder="输入您的需求描述..."
            class="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none transition-all duration-200 shadow-sm"
            rows="1"
            :disabled="disabled"
            @keydown="handleKeydown"
            @input="adjustTextareaHeight"
          />
        </div>

        <!-- 发送按钮 -->
        <div class="flex-shrink-0 self-end">
          <button
            @click="handleSend"
            :disabled="disabled || !canSend"
            class="inline-flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-200 shadow-sm"
            :class="{
              'bg-primary-600 hover:bg-primary-700 text-white hover:scale-105 active:scale-95': canSend && !disabled,
              'bg-gray-300 text-gray-500 cursor-not-allowed': !canSend || disabled
            }"
          >
            <PaperAirplaneIcon class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- 提示文本 -->
    <div class="mt-2 text-xs text-gray-600 flex items-center justify-between">
      <span>支持文本描述和图片上传</span>
      <span>Shift + Enter 换行，Enter 发送</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { PhotoIcon, PaperAirplaneIcon } from '@heroicons/vue/24/outline'

const emit = defineEmits(['send-message'])

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const inputText = ref('')
const selectedImage = ref(null)
const imageFile = ref(null)
const textareaRef = ref(null)

const canSend = computed(() => {
  return inputText.value.trim() || selectedImage.value
})

function handleImageSelect(event) {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
    selectedImage.value = URL.createObjectURL(file)
  }
}

function removeImage() {
  selectedImage.value = null
  imageFile.value = null
  // 清除文件输入
  const input = document.getElementById('image-upload')
  if (input) {
    input.value = ''
  }
}

function handleSend() {
  if (!canSend.value || props.disabled) return

  const content = inputText.value.trim()
  const image = imageFile.value

  if (content || image) {
    emit('send-message', {
      content: content || '请分析这张图片',
      imageFile: image
    })

    // 清空输入
    inputText.value = ''
    removeImage()
    
    // 重置textarea高度
    nextTick(() => {
      adjustTextareaHeight()
    })
  }
}

function handleKeydown(event) {
  if (event.key === 'Enter') {
    if (event.shiftKey) {
      // Shift + Enter 换行
      return
    } else {
      // Enter 发送
      event.preventDefault()
      handleSend()
    }
  }
}

function adjustTextareaHeight() {
  const textarea = textareaRef.value
  if (textarea) {
    textarea.style.height = 'auto'
    const scrollHeight = textarea.scrollHeight
    const maxHeight = 120 // 最大高度
    textarea.style.height = Math.min(scrollHeight, maxHeight) + 'px'
  }
}
</script> 