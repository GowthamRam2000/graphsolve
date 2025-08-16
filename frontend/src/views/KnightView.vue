<template>
  <div class="knight-view">
    <h1>Knight's Tour</h1>
    <p>Navigate a knight to visit every square exactly once using Hamiltonian path algorithms</p>

    <div class="puzzle-container">
      <div class="puzzle-board">
        <ChessBoard
          :size="parseInt(boardSize)"
          :pieces="currentPosition ? [currentPosition] : []"
          pieceType="knight"
          :path="tourPath"
          :showNumbers="true"
          :interactive="true"
          @cellClick="setStartPosition"
        />

        <div class="button-group">
          <button class="btn-primary" @click="solveTour" :disabled="isLoading">
            <span class="material-icons">play_arrow</span>
            {{ isLoading ? 'Finding...' : 'Find Tour' }}
          </button>
          <button class="btn-secondary" @click="clearTour">
            <span class="material-icons">clear</span>
            Clear
          </button>
          <button class="btn-secondary" @click="animateTour" :disabled="!tourPath.length">
            <span class="material-icons">animation</span>
            Animate
          </button>
        </div>
      </div>

      <div class="puzzle-controls">
        <div class="controls-card">
          <h3>Board Size</h3>
          <div class="slider-container">
            <input
              type="range"
              v-model.number="boardSize"
              min="5"
              max="8"
              step="1"
              class="slider"
              :disabled="isLoading"
            />
            <div class="slider-label">{{ boardSize }}×{{ boardSize }} board</div>
          </div>
        </div>

        <div class="controls-card">
          <h3>Algorithm</h3>
          <select v-model="algorithm" class="select-field">
            <option v-for="algo in algorithms" :key="algo.value" :value="algo.value">
              {{ algo.label }}
            </option>
          </select>
        </div>

        <div class="controls-card">
          <h3>Tour Type</h3>
          <div class="radio-group">
            <label class="radio-container">
              <input type="radio" v-model="tourType" value="open" />
              <span class="radio-mark"></span>
              Open Tour
            </label>
            <label class="radio-container">
              <input type="radio" v-model="tourType" value="closed" />
              <span class="radio-mark"></span>
              Closed Tour
            </label>
          </div>
        </div>

        <div class="controls-card">
          <h3>Starting Position</h3>
          <div class="position-display">
            Row: {{ startPosition[0] + 1 }}, Col: {{ startPosition[1] + 1 }}
          </div>
          <p class="hint">Click on the board to set start position</p>
        </div>

        <div class="controls-card">
          <h3>Options</h3>
          <label class="checkbox-container">
            <input type="checkbox" v-model="returnSteps" />
            <span class="checkmark"></span>
            Show solution steps
          </label>
        </div>

        <div v-if="statistics" class="stats-card">
          <h3>Solution Statistics</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ formatTime(statistics.time_ms) }}</div>
              <div class="stat-label">TIME</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ statistics.nodes_explored }}</div>
              <div class="stat-label">NODES</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ statistics.algorithm_used }}</div>
              <div class="stat-label">ALGORITHM</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ tourPath.length }}</div>
              <div class="stat-label">MOVES</div>
            </div>
          </div>
        </div>

        <div v-if="steps.length > 0" class="steps-card">
          <div class="steps-header">
            <h3>Solution Steps</h3>
            <span class="step-count">{{ steps.length }} steps</span>
          </div>
          <div class="steps-controls">
            <button class="step-btn" @click="prevStep" :disabled="currentStep === 0">
              <span class="material-icons">skip_previous</span>
            </button>
            <button class="step-btn" @click="togglePlay">
              <span class="material-icons">{{ isPlaying ? 'pause' : 'play_arrow' }}</span>
            </button>
            <button class="step-btn" @click="nextStep" :disabled="currentStep >= steps.length - 1">
              <span class="material-icons">skip_next</span>
            </button>
            <span class="step-indicator">{{ currentStep + 1 }} / {{ steps.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p>Finding tour...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch } from 'vue'
import { usePuzzleStore } from '../stores/puzzle'
import { delay, formatTime } from '../utils/helpers'
import ChessBoard from '../components/ChessBoard.vue'

const store = usePuzzleStore()

const boardSize = ref(6)
const startPosition = ref([0, 0])
const currentPosition = ref([0, 0])
const tourPath = ref([])
const steps = ref([])
const statistics = ref(null)
const isLoading = ref(false)
const algorithm = ref('warnsdorff')
const tourType = ref('open')
const returnSteps = ref(true)
const currentStep = ref(0)
const isPlaying = ref(false)
const playInterval = ref(null)

// Watch boardSize changes and reset
watch(boardSize, (newSize) => {
  const size = parseInt(newSize)
  startPosition.value = [0, 0]
  currentPosition.value = [0, 0]
  clearTour()
})

const algorithms = [
  { value: 'warnsdorff', label: "Warnsdorff's Heuristic" },
  { value: 'backtracking', label: 'Backtracking' }
]

const setStartPosition = (position) => {
  // Ensure position values are integers
  startPosition.value = [parseInt(position[0]), parseInt(position[1])]
  currentPosition.value = [parseInt(position[0]), parseInt(position[1])]
  clearTour()
}

const solveTour = async () => {
  try {
    isLoading.value = true
    tourPath.value = []
    store.setAlgorithm(algorithm.value)
    store.setReturnSteps(returnSteps.value)

    // Ensure all values are integers
    const size = parseInt(boardSize.value)
    const start = [parseInt(startPosition.value[0]), parseInt(startPosition.value[1])]

    const result = await store.solveKnight(
      size,
      start,
      tourType.value === 'closed',
      algorithm.value
    )

    if (result.success) {
      tourPath.value = result.solution
      steps.value = result.steps || []
      statistics.value = result.statistics

      if (tourPath.value.length === size * size) {
        if (tourType.value === 'closed') {
          alert('Found a closed tour!')
        } else {
          alert('Found a complete tour!')
        }
      }
    } else {
      alert('No tour found from this position!')
    }
  } catch (error) {
    console.error('Error solving tour:', error)
    alert('Error solving tour: ' + (error.response?.data?.detail || error.message))
  } finally {
    isLoading.value = false
  }
}

const animateTour = async () => {
  if (!tourPath.value.length) return

  const tempPath = [...tourPath.value]
  tourPath.value = []
  currentPosition.value = tempPath[0]

  for (let i = 0; i < tempPath.length; i++) {
    tourPath.value = tempPath.slice(0, i + 1)
    currentPosition.value = tempPath[i]
    await delay(200)
  }
}

const clearTour = () => {
  tourPath.value = []
  steps.value = []
  statistics.value = null
  currentPosition.value = startPosition.value
  currentStep.value = 0
}

const nextStep = () => {
  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    playInterval.value = setInterval(() => {
      if (currentStep.value < steps.value.length - 1) {
        nextStep()
      } else {
        isPlaying.value = false
        clearInterval(playInterval.value)
      }
    }, 500)
  } else {
    clearInterval(playInterval.value)
  }
}

onUnmounted(() => {
  if (playInterval.value) {
    clearInterval(playInterval.value)
  }
})
</script>

<style scoped>
.knight-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.knight-view h1 {
  color: #1976d2;
  margin-bottom: 8px;
  font-size: 32px;
}

.knight-view > p {
  color: #666;
  margin-bottom: 24px;
  font-size: 16px;
}

.puzzle-container {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
}

.puzzle-board {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.puzzle-controls {
  width: 380px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.button-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-primary, .btn-secondary {
  padding: 12px 24px;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary {
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
}

.btn-secondary:hover {
  background: #f5f5f5;
  border-color: #4CAF50;
  color: #4CAF50;
}

.controls-card, .stats-card, .steps-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.controls-card h3, .stats-card h3, .steps-card h3 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 18px;
}

.slider-container {
  width: 100%;
}

.slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: #e0e0e0;
  outline: none;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4CAF50;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4CAF50;
  cursor: pointer;
  border: none;
}

.slider-label {
  text-align: center;
  margin-top: 12px;
  color: #666;
  font-weight: 500;
}

.select-field {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.select-field:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  position: relative;
  padding-left: 32px;
}

.radio-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.radio-mark {
  position: absolute;
  top: 0;
  left: 0;
  height: 22px;
  width: 22px;
  background-color: white;
  border: 2px solid #ddd;
  border-radius: 50%;
  transition: all 0.3s;
}

.radio-container:hover .radio-mark {
  border-color: #4CAF50;
}

.radio-container input:checked ~ .radio-mark {
  background-color: #4CAF50;
  border-color: #4CAF50;
}

.radio-mark:after {
  content: "";
  position: absolute;
  display: none;
  top: 6px;
  left: 6px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: white;
}

.radio-container input:checked ~ .radio-mark:after {
  display: block;
}

.position-display {
  padding: 16px;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
  font-size: 16px;
  color: #333;
}

.hint {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
  text-align: center;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  position: relative;
  padding-left: 32px;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 22px;
  width: 22px;
  background-color: white;
  border: 2px solid #ddd;
  border-radius: 4px;
  transition: all 0.3s;
}

.checkbox-container:hover .checkmark {
  border-color: #4CAF50;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #4CAF50;
  border-color: #4CAF50;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 7px;
  top: 3px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.stat-item {
  text-align: center;
  padding: 12px 8px;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  border-radius: 8px;
  min-height: 70px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #4CAF50;
  margin-bottom: 4px;
  word-break: break-all;
  line-height: 1.2;
}

.stat-label {
  font-size: 11px;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.steps-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.step-count {
  color: #999;
  font-size: 14px;
}

.steps-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 8px;
}

.step-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.step-btn:hover:not(:disabled) {
  background: #4CAF50;
  color: white;
}

.step-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.step-indicator {
  margin-left: auto;
  color: #666;
  font-size: 14px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
  color: white;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255,255,255,0.3);
  border-top-color: #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.material-icons {
  font-size: 20px;
}
</style>