<template>
  <div class="info-card">
    <h3 class="section-title">{{ title }}</h3>
    <div class="info-grid">
      <div v-for="(value, key) in items" :key="key" class="info-item">
        <div class="info-label">{{ getLabel(key) }}</div>
        <div class="info-value">{{ value || '-' }}</div>
      </div>
    </div>
    <div v-if="longText" class="long-text-section">
      <div class="info-label">{{ longTextLabel }}</div>
      <div class="text-content">{{ longText || '-' }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  items: Record<string, string | null>
  longText?: string | null
  longTextLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  longTextLabel: '详情'
})

const labelMap: Record<string, string> = {
  name: '姓名',
  phone: '电话',
  email: '邮箱',
  address: '地址',
  job_intention: '求职意向',
  expected_salary: '期望薪资',
  work_years: '工作年限',
  education: '学历背景',
  projects: '项目经历'
}

const getLabel = (key: string): string => {
  return labelMap[key] || key
}
</script>

<style scoped>
.info-card {
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.info-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
}

.info-label {
  font-size: 0.85em;
  color: #666;
  margin-bottom: 5px;
}

.info-value {
  font-size: 1.1em;
  color: #333;
  font-weight: 500;
}

.long-text-section {
  margin-top: 20px;
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
  margin-top: 10px;
}
</style>
