<template>
  <div class="app">
    <div class="container">
      <div class="header">
        <h1>📄 简历分析系统</h1>
        <p>智能解析简历，精准匹配岗位</p>
      </div>

      <div class="card">
        <h2 class="section-title">📤 上传简历</h2>
        <FileUpload @file-selected="handleFileSelected" />
      </div>

      <div class="card">
        <h2 class="section-title">💼 岗位需求</h2>
        <textarea class="textarea" 
                  v-model="jobRequirement"
                  placeholder="请输入岗位需求描述..."></textarea>
        <div class="button-container">
          <button class="btn" 
                  :disabled="!selectedFile"
                  @click="handleAnalyze">
            开始分析
          </button>
        </div>
      </div>

      <div class="loading" :class="{ show: isLoading }">
        <div class="spinner"></div>
        <p>正在分析中，请稍候...</p>
      </div>

      <div v-if="result" class="result-section">
        <div class="card">
          <h2 class="section-title">📊 匹配评分</h2>
          <ScoreDisplay 
            :score="result.match_score.overall_score"
            :skill-match-rate="result.match_score.skill_match_rate"
            :content-similarity="result.match_score.content_similarity"
            :matched-keywords="result.match_score.matched_keywords" />
        </div>

        <InfoCard title="👤 基本信息" :items="result.info.basic_info" />
        <InfoCard title="🎯 求职信息" :items="result.info.job_info" />
        <InfoCard 
          title="📚 背景信息" 
          :items="omitProjects(result.info.background_info)"
          :long-text="result.info.background_info.projects"
          long-text-label="项目经历" />

        <div class="card">
          <h2 class="section-title">📝 简历原文</h2>
          <div class="text-content">{{ result.raw_text }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import FileUpload from './components/FileUpload.vue'
import ScoreDisplay from './components/ScoreDisplay.vue'
import InfoCard from './components/InfoCard.vue'
import type { AnalysisResult } from './types'

const selectedFile = ref<File | null>(null)
const jobRequirement = ref('')
const isLoading = ref(false)
const result = ref<AnalysisResult | null>(null)

const handleFileSelected = (file: File) => {
  selectedFile.value = file
}

const handleAnalyze = async () => {
  if (!selectedFile.value) return

  isLoading.value = true
  result.value = null

  const formData = new FormData()
  formData.append('resume', selectedFile.value)
  formData.append('job_requirement', jobRequirement.value)

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    if (data.success) {
      result.value = data.data
    } else {
      alert('分析失败：' + data.message)
    }
  } catch (error) {
    alert('请求失败：' + (error as Error).message)
  } finally {
    isLoading.value = false
  }
}

const omitProjects = (obj: any) => {
  const { projects, ...rest } = obj
  return rest
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft YaHei', sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

#app {
  min-height: 100vh;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.card {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.section-title {
  font-size: 1.3em;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #667eea;
}

.textarea {
  width: 100%;
  min-height: 150px;
  padding: 15px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1em;
  resize: vertical;
  transition: border-color 0.3s;
}

.textarea:focus {
  outline: none;
  border-color: #667eea;
}

.button-container {
  margin-top: 20px;
  text-align: center;
}

.btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 1em;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading {
  display: none;
  text-align: center;
  padding: 20px;
}

.loading.show {
  display: block;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.result-section {
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.text-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
  font-size: 0.95em;
  line-height: 1.6;
}
</style>
