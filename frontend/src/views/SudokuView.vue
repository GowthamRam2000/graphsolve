<template>
  <div class="sudoku-view">
    <h1>Sudoku Solver</h1>
    <p>Solve Sudoku puzzles using graph coloring and constraint propagation</p>

    <div class="puzzle-container">
      <div class="puzzle-board">
        <SudokuGrid
          v-model="grid"
          :solution="solution"
          :originalCells="originalCells"
          :disabled="isLoading"
          :isAnimating="animateSolution"
          @animationComplete="onAnimationComplete"
        />

        <div class="button-group">
          <button class="btn-primary" @click="solvePuzzle" :disabled="isLoading">
            <span class="material-icons">play_arrow</span>
            {{ isLoading ? 'Solving...' : 'Solve' }}
          </button>
          <button class="btn-secondary" @click="clearGrid">
            <span class="material-icons">clear</span>
            Clear
          </button>
          <button class="btn-secondary" @click="resetGrid">
            <span class="material-icons">refresh</span>
            Reset
          </button>
        </div>
      </div>

      <div class="puzzle-controls">
        <div class="controls-card">
          <h3>Presets</h3>
          <div class="difficulty-buttons">
            <button
              v-for="level in difficulties"
              :key="level"
              @click="loadPreset(level)"
              :class="['difficulty-btn', { 'active': difficulty === level }]"
            >
              {{ level }}
            </button>
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
          <h3>Options</h3>
          <label class="checkbox-container">
            <input type="checkbox" v-model="returnSteps" />
            <span class="checkmark"></span>
            Show solution steps
          </label>
          <label class="checkbox-container">
            <input type="checkbox" v-model="animateSolution" />
            <span class="checkmark"></span>
            Animate solution
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
              <div class="stat-label">NODES EXPLORED</div>
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

        <div v-if="steps.length > 0 && !animateSolution" class="steps-card">
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
          <div class="steps-list">
            <div
              v-for="(step, index) in visibleSteps"
              :key="index"
              :class="['step-item', { 'active': index === currentStep }]"
            >
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-content">
                <div class="step-action">{{ step.action }}</div>
                <div class="step-description">{{ step.description }}</div>
              </div>
            </div>
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
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { usePuzzleStore } from '../stores/puzzle'
import { puzzleAPI } from '../services/api'
import { createEmptySudoku, formatTime } from '../utils/helpers'
import SudokuGrid from '../components/SudokuGrid.vue'

const store = usePuzzleStore()

const grid = ref(createEmptySudoku())
const originalGrid = ref(null)
const originalCells = ref(Array(9).fill(null).map(() => Array(9).fill(false)))
const solution = ref(null)
const steps = ref([])
const statistics = ref(null)
const isLoading = ref(false)
const difficulty = ref('easy')
const algorithm = ref('backtracking')
const returnSteps = ref(true)
const animateSolution = ref(true)
const currentStep = ref(0)
const isPlaying = ref(false)
const playInterval = ref(null)

const difficulties = ['easy', 'medium', 'hard']

const algorithms = [
  { value: 'backtracking', label: 'Backtracking' },
  { value: 'constraint_propagation', label: 'Constraint Propagation' }
]

const visibleSteps = computed(() => {
  const start = Math.max(0, currentStep.value - 2)
  const end = Math.min(steps.value.length, start + 5)
  return steps.value.slice(start, end)
})

const solvePuzzle = async () => {
  try {
    isLoading.value = true
    solution.value = null
    steps.value = []
    statistics.value = null
    currentStep.value = 0

    store.setAlgorithm(algorithm.value)
    store.setReturnSteps(returnSteps.value)

    const result = await store.solveSudoku(grid.value, algorithm.value)

    if (result.success) {
      solution.value = result.solution
      steps.value = result.steps || []
      statistics.value = result.statistics
    } else {
      alert('No solution found!')
    }
  } catch (error) {
    console.error('Error solving puzzle:', error)
    alert('Error solving puzzle')
  } finally {
    isLoading.value = false
  }
}

const clearGrid = () => {
  grid.value = createEmptySudoku()
  originalCells.value = Array(9).fill(null).map(() => Array(9).fill(false))
  solution.value = null
  steps.value = []
  statistics.value = null
  currentStep.value = 0
}

const resetGrid = () => {
  if (originalGrid.value) {
    grid.value = originalGrid.value.map(row => [...row])
  }
  solution.value = null
  steps.value = []
  statistics.value = null
  currentStep.value = 0
}

const loadPreset = async (level) => {
  difficulty.value = level
  try {
    const response = await puzzleAPI.getPresets('sudoku')
    const preset = response.data.find(p => p.difficulty === level)

    if (preset) {
      grid.value = preset.data.grid.map(row => [...row])
      originalGrid.value = preset.data.grid.map(row => [...row])
      originalCells.value = preset.data.grid.map(row =>
        row.map(cell => cell !== 0)
      )
      solution.value = null
      steps.value = []
      statistics.value = null
      currentStep.value = 0
    }
  } catch (error) {
    console.error('Error loading preset:', error)
  }
}

const onAnimationComplete = () => {
  // Animation completed
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

onMounted(() => {
  loadPreset('easy')
})

onUnmounted(() => {
  if (playInterval.value) {
    clearInterval(playInterval.value)
  }
})
</script>

<style scoped>
.sudoku-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.sudoku-view h1 {
  color: #1976d2;
  margin-bottom: 8px;
  font-size: 32px;
}

.sudoku-view > p {
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
  transition: all 0.3s;
}

.controls-card:hover, .stats-card:hover, .steps-card:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,0.12);
}

.controls-card h3, .stats-card h3, .steps-card h3 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 18px;
}

.difficulty-buttons {
  display: flex;
  gap: 8px;
}

.difficulty-btn {
  flex: 1;
  padding: 10px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: capitalize;
  font-weight: 500;
}

.difficulty-btn:hover {
  border-color: #4CAF50;
  background: #E8F5E9;
}

.difficulty-btn.active {
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  color: white;
  border-color: transparent;
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

.steps-list {
  max-height: 300px;
  overflow-y: auto;
}

.step-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  background: #f9f9f9;
  transition: all 0.3s;
}

.step-item.active {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
}

.step-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #4CAF50;
  color: white;
  border-radius: 50%;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-action {
  font-weight: 500;
  color: #333;
  text-transform: capitalize;
}

.step-description {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
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
