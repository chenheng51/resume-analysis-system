<template>
  <div class="score-display">
    <div class="score-circle" :style="circleStyle">
      <div class="score-inner">
        <div class="score-number">{{ animatedScore.toFixed(1) }}</div>
        <div class="score-label">匹配度</div>
      </div>
    </div>
    <div class="info-grid">
      <div class="info-item">
        <div class="info-label">技能匹配率</div>
        <div class="info-value">{{ skillMatchRate }}%</div>
      </div>
      <div class="info-item">
        <div class="info-label">内容相似度</div>
        <div class="info-value">{{ contentSimilarity }}%</div>
      </div>
    </div>
    <div class="keywords-section">
      <div class="info-label">匹配关键词</div>
      <div class="keywords">
        <span v-for="(keyword, index) in matchedKeywords" :key="index" class="keyword">
          {{ keyword }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

interface Props {
  score: number
  skillMatchRate: number
  contentSimilarity: number
  matchedKeywords: string[]
}

const props = defineProps<Props>()

const animatedScore = ref(0)

const circleStyle = computed(() => ({
  '--percent': props.score + '%'
}))

watch(() => props.score, (newScore) => {
  animateScore(newScore)
})

const animateScore = (target: number) => {
  animatedScore.value = 0
  const increment = target / 50
  const timer = setInterval(() => {
    animatedScore.value += increment
    if (animatedScore.value >= target) {
      animatedScore.value = target
      clearInterval(timer)
    }
  }, 20)
}

onMounted(() => {
  animateScore(props.score)
})
</script>

<style scoped>
.score-display {
  text-align: center;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: conic-gradient(#667eea var(--percent), #e0e0e0 var(--percent));
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto;
}

.score-inner {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.score-number {
  font-size: 2em;
  font-weight: bold;
  color: #667eea;
}

.score-label {
  font-size: 0.9em;
  color: #666;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 20px 0;
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

.keywords-section {
  margin-top: 20px;
}

.keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
  justify-content: center;
}

.keyword {
  background: #e0e7ff;
  color: #667eea;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9em;
}
</style>
