<template>
  <md-outlined-card v-if="steps && steps.length > 0">
    <div class="steps-container">
      <div class="steps-header">
        <h3>Solution Steps</h3>
        <span class="step-count">{{ steps.length }} steps</span>
      </div>
      <div class="steps-controls" v-if="showControls">
        <md-icon-button @click="prevStep" :disabled="currentStep === 0">
          <md-icon>skip_previous</md-icon>
        </md-icon-button>
        <md-icon-button @click="togglePlay">
          <md-icon>{{ isPlaying ? 'pause' : 'play_arrow' }}</md-icon>
        </md-icon-button>
        <md-icon-button @click="nextStep" :disabled="currentStep >= steps.length - 1">
          <md-icon>skip_next</md-icon>
        </md-icon-button>
        <span class="step-indicator">{{ currentStep + 1 }} / {{ steps.length }}</span>
      </div>
      <div class="steps-list" ref="stepsList">
        <div
          v-for="(step, index) in steps"
          :key="index"
          :class="{ 'active': index === currentStep }"
          class="step-item"
        >
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-content">
            <div class="step-action">{{ step.action }}</div>
            <div class="step-description">{{ step.description }}</div>
          </div>
        </div>
      </div>
    </div>
  </md-outlined-card>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
  steps: {
    type: Array,
    default: () => []
  },
  showControls: {
    type: Boolean,
    default: false
  },
  autoPlay: {
    type: Boolean,
    default: false
  },
  playSpeed: {
    type: Number,
    default: 1000
  }
})

const emit = defineEmits(['stepChange'])

const currentStep = ref(0)
const isPlaying = ref(false)
const playInterval = ref(null)
const stepsList = ref(null)

const nextStep = () => {
  if (currentStep.value < props.steps.length - 1) {
    currentStep.value++
    emit('stepChange', currentStep.value)
    scrollToStep()
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
    emit('stepChange', currentStep.value)
    scrollToStep()
  }
}

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    startAutoPlay()
  } else {
    stopAutoPlay()
  }
}

const startAutoPlay = () => {
  playInterval.value = setInterval(() => {
    if (currentStep.value < props.steps.length - 1) {
      nextStep()
    } else {
      stopAutoPlay()
    }
  }, props.playSpeed)
}

const stopAutoPlay = () => {
  if (playInterval.value) {
    clearInterval(playInterval.value)
    playInterval.value = null
    isPlaying.value = false
  }
}

const scrollToStep = () => {
  if (stepsList.value) {
    const activeStep = stepsList.value.querySelector('.step-item.active')
    if (activeStep) {
      activeStep.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }
}

watch(() => props.autoPlay, (newVal) => {
  if (newVal) {
    startAutoPlay()
  } else {
    stopAutoPlay()
  }
})

onUnmounted(() => {
  stopAutoPlay()
})
</script>

<style scoped>
.steps-container {
  padding: 16px;
}

.steps-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.steps-header h3 {
  margin: 0;
  color: var(--md-sys-color-on-surface);
}

.step-count {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 14px;
}

.steps-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.step-indicator {
  margin-left: 8px;
  color: var(--md-sys-color-on-surface-variant);
}

.steps-list {
  max-height: 400px;
  overflow-y: auto;
}

.step-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  background: var(--md-sys-color-surface);
  border: 1px solid var(--md-sys-color-outline);
  transition: all 0.3s;
}

.step-item.active {
  background: var(--md-sys-color-primary-container);
  border-color: var(--md-sys-color-primary);
}

.step-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border-radius: 50%;
  font-weight: 500;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-action {
  font-weight: 500;
  color: var(--md-sys-color-on-surface);
  text-transform: capitalize;
}

.step-description {
  font-size: 14px;
  color: var(--md-sys-color-on-surface-variant);
  margin-top: 4px;
}
</style>