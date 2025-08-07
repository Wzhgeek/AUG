<template>
  <div class="h-screen bg-gray-100 flex overflow-hidden">
    <!-- 左侧控制台 (20%) -->
    <div class="w-1/5 bg-white border-r border-gray-300 flex flex-col rounded-r-2xl shadow-lg">
      <SidebarPanel />
    </div>
    
    <!-- 右侧主要内容区 (80%) -->
    <div class="flex-1 flex">
      <!-- 对话区域 -->
      <div class="flex-1 flex flex-col">
        <ChatArea />
      </div>
      
      <!-- 详情侧边栏 -->
      <Transition
        enter-active-class="transition-transform duration-300 ease-out"
        enter-from-class="transform translate-x-full"
        enter-to-class="transform translate-x-0"
        leave-active-class="transition-transform duration-300 ease-in"
        leave-from-class="transform translate-x-0"
        leave-to-class="transform translate-x-full"
      >
        <div 
          v-if="showDetailSidebar" 
          class="w-96 bg-white border-l border-gray-300 rounded-l-2xl shadow-lg"
        >
          <DetailSidebar />
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useChatStore } from '../stores/chat.js'
import SidebarPanel from './SidebarPanel.vue'
import ChatArea from './ChatArea.vue'
import DetailSidebar from './DetailSidebar.vue'

const chatStore = useChatStore()
const { showDetailSidebar } = storeToRefs(chatStore)
</script> 