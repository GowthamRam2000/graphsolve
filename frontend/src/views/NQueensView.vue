<template>
  <div class="nqueens-view">
    <h1>N-Queens Solver</h1>
    <p>Place N queens on an N×N chessboard using constraint satisfaction</p>

    <div class="puzzle-container">
      <div class="puzzle-board">
        <ChessBoard
          :size="parseInt(boardSize)"
          :pieces="queens"
          pieceType="queen"
          :interactive="true"
          @cellClick="toggleQueen"
        />

        <div class="button-group">
          <button class="btn-primary" @click="solvePuzzle" :disabled="isLoading">
            <span class="material-icons">play_arrow</span>
            {{ isLoading ? 'Solving...' : 'Solve' }}
          </button>
          <button class="btn-secondary" @click="clearBoard">
            <span class="material-icons">clear</span>
            Clear
          </button>
          <button class="btn-secondary" @click="findAllSolutions">
            <span class="material-icons">search</span>
            All Solutions
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
              min="4"
              max="12"
              step="1"
              class="slider"
              :disabled="isLoading"
            />
            <div class="slider-label">{{ boardSize }}×{{ boardSize }} board</div>
          </div>
        </div>

        <div class="controls-card">
          <h3>Options</h3>
          <label class="checkbox-container">
            <input type="checkbox" v-model="returnSteps" />
            <span class="checkmark"></span>
            Show solution steps
          </label>
        </div>

        <div v-if="allSolutions.length > 0" class="controls-card">
          <h3>Solutions ({{ allSolutions.length }})</h3>
          <div class="solutions-list">
            <button
              v-for="(sol, index) in allSolutions"
              :key="index"
              class="solution-btn"
              @click="showSolution(sol)"
            >
              Solution {{ index + 1 }}
            </button>
          </div>
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
              <div class="stat-value">{{ statistics.backtrack_count || 0 }}</div>
              <div class="stat-label">BACKTRACKS</div>
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
        <p>Solving puzzle...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch } from 'vue'
import { usePuzzleStore } from '../stores/puzzle'
import { formatTime } from '../utils/helpers'
import ChessBoard from '../components/ChessBoard.vue'

const store = usePuzzleStore()

const boardSize = ref(8)

// Watch boardSize changes and clear the board
watch(boardSize, () => {
  queens.value = []
  presetQueens.value = []
  allSolutions.value = []
  steps.value = []
  statistics.value = null
  currentStep.value = 0
})
const queens = ref([])
const presetQueens = ref([])
const allSolutions = ref([])
const steps = ref([])
const statistics = ref(null)
const isLoading = ref(false)
const returnSteps = ref(true)
const currentStep = ref(0)
const isPlaying = ref(false)
const playInterval = ref(null)

const toggleQueen = (position) => {
  const index = queens.value.findIndex(([r, c]) => r === position[0] && c === position[1])
  if (index >= 0) {
    queens.value.splice(index, 1)
  } else {
    queens.value.push(position)
  }
  presetQueens.value = [...queens.value]
}

const solvePuzzle = async () => {
  try {
    isLoading.value = true
    store.setReturnSteps(returnSteps.value)

    // Ensure boardSize is an integer
    const size = parseInt(boardSize.value)

    const result = await store.solveNQueens(size, presetQueens.value, 1)

    if (result.success) {
      queens.value = result.solution
      steps.value = result.steps || []
      statistics.value = result.statistics
    } else {
      alert('No solution found!')
    }
  } catch (error) {
    console.error('Error solving puzzle:', error)
    alert('Error solving puzzle: ' + (error.response?.data?.detail || error.message))
  } finally {
    isLoading.value = false
  }
}

const findAllSolutions = async () => {
  try {
    isLoading.value = true
    store.setReturnSteps(false)

    // Ensure boardSize is an integer
    const size = parseInt(boardSize.value)

    const result = await store.solveNQueens(size, [], 100)

    if (result.success) {
      allSolutions.value = result.solution
      statistics.value = result.statistics
      alert(`Found ${allSolutions.value.length} solutions`)
    } else {
      alert('No solutions found!')
    }
  } catch (error) {
    console.error('Error finding solutions:', error)
    alert('Error finding solutions: ' + (error.response?.data?.detail || error.message))
  } finally {
    isLoading.value = false
  }
}

const showSolution = (sol) => {
  queens.value = sol
  steps.value = []
}

const clearBoard = () => {
  queens.value = []
  presetQueens.value = []
  allSolutions.value = []
  steps.value = []
  statistics.value = null
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
.nqueens-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.nqueens-view h1 {
  color: #1976d2;
  margin-bottom: 8px;
  font-size: 32px;
}

.nqueens-view > p {
  color: #666;
  margin-bottom: 24px;
  font-size: 16px;
}

.puzzle-container {
  display: flex;
  gap: 32px;
}

.puzzle-board {
  flex: 1;
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

.checkbox-container {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
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

.solutions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.solution-btn {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.solution-btn:hover {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
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