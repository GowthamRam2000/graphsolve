<template>
  <md-outlined-card v-if="statistics">
    <div class="stats-container">
      <h3>Solution Statistics</h3>
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{{ formatTime(statistics.time_ms) }}</div>
          <div class="stat-label">Time</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ formatNumber(statistics.nodes_explored) }}</div>
          <div class="stat-label">Nodes Explored</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ statistics.algorithm_used }}</div>
          <div class="stat-label">Algorithm</div>
        </div>
        <div v-if="statistics.backtrack_count !== undefined" class="stat-item">
          <div class="stat-value">{{ formatNumber(statistics.backtrack_count) }}</div>
          <div class="stat-label">Backtracks</div>
        </div>
      </div>
    </div>
  </md-outlined-card>
</template>

<script setup>
import { formatTime, formatNumber } from '../utils/helpers'

defineProps({
  statistics: {
    type: Object,
    default: null
  }
})
</script>

<style scoped>
.stats-container {
  padding: 16px;
}

.stats-container h3 {
  margin-bottom: 16px;
  color: var(--md-sys-color-on-surface);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  background: var(--md-sys-color-surface-variant);
  border-radius: 8px;
}

.stat-value {
  font-size: 20px;
  font-weight: 500;
  color: var(--md-sys-color-primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--md-sys-color-on-surface-variant);
  text-transform: uppercase;
}
</style>