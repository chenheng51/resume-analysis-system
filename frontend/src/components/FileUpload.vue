<template>
  <div class="upload-area" 
       :class="{ dragover: isDragover }"
       @click="handleClick"
       @dragover.prevent="isDragover = true"
       @dragleave="isDragover = false"
       @drop.prevent="handleDrop">
    <input type="file" 
           ref="fileInput"
           accept=".pdf" 
           @change="handleFileChange"
           class="file-input">
    <div v-if="!selectedFile" class="upload-prompt">
      <div class="icon">📁</div>
      <p>点击或拖拽上传 PDF 简历</p>
    </div>
    <div v-else class="file-info">
      <div class="icon">✅</div>
      <p class="filename">{{ selectedFile.name }}</p>
      <p class="filesize">{{ formatFileSize(selectedFile.size) }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'file-selected', file: File): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const isDragover = ref(false)

const handleClick = () => {
  fileInput.value?.click()
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectFile(target.files[0])
  }
}

const handleDrop = (e: DragEvent) => {
  isDragover.value = false
  if (e.dataTransfer && e.dataTransfer.files[0]) {
    selectFile(e.dataTransfer.files[0])
  }
}

const selectFile = (file: File) => {
  if (file.type !== 'application/pdf') {
    alert('请上传 PDF 格式的文件')
    return
  }
  selectedFile.value = file
  emit('file-selected', file)
}

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}
</script>

<style scoped>
.upload-area {
  border: 3px dashed #667eea;
  border-radius: 10px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-area:hover {
  background: #f0f4ff;
}

.upload-area.dragover {
  background: #e0e7ff;
  border-color: #764ba2;
}

.file-input {
  display: none;
}

.upload-prompt .icon,
.file-info .icon {
  font-size: 3em;
  margin-bottom: 10px;
}

.file-info .filename {
  font-weight: 500;
  margin-bottom: 5px;
}

.file-info .filesize {
  color: #666;
  font-size: 0.9em;
}
</style>
