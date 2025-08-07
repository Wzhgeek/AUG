<template>
  <div 
    class="bg-white border border-gray-200 rounded-xl p-4 cursor-pointer hover:border-primary-500 hover:shadow-lg transition-all duration-200 group"
    @click="$emit('click')"
  >
    <div class="flex items-start space-x-3">
      <!-- 图片预览 -->
      <div class="flex-shrink-0">
        <div class="relative">
          <img
            v-if="plantumlResult.image_url"
            :src="getImageUrl(plantumlResult.image_url)"
            alt="生成的UML图"
            class="w-24 h-24 object-cover rounded-xl border border-gray-300 shadow-sm"
          />
                     <div v-else class="w-24 h-24 bg-gray-100 rounded-xl flex items-center justify-center">
             <DocumentIcon class="w-8 h-8 text-gray-500" />
           </div>
          
          <!-- 点击查看提示 -->
          <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 rounded-xl flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all">
            <EyeIcon class="w-6 h-6 text-white" />
          </div>
        </div>
      </div>

      <!-- 详情信息 -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-sm font-medium text-gray-900">UML图表</h4>
          <div class="flex items-center space-x-1">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span class="text-xs text-green-400">生成成功</span>
          </div>
        </div>
        
        <p class="text-xs text-gray-600 mb-2">
          点击查看详细的UML代码和高清图片
        </p>
        
        <div class="flex items-center justify-between">
          <div class="flex items-center text-xs text-gray-600">
            <ClockIcon class="w-3 h-3 mr-1" />
            刚刚生成
          </div>
          
          <div class="flex items-center text-xs text-primary-400 group-hover:text-primary-300">
            <span>查看详情</span>
            <ChevronRightIcon class="w-3 h-3 ml-1" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  DocumentIcon, 
  EyeIcon, 
  ClockIcon, 
  ChevronRightIcon 
} from '@heroicons/vue/24/outline'

defineProps({
  plantumlResult: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

function getImageUrl(url) {
  // 如果URL已经是完整的HTTP URL，直接返回
  if (url && url.startsWith('http')) {
    return url
  }
  // 否则添加localhost前缀（用于本地开发）
  return `http://localhost:8078${url}`
}
</script> 