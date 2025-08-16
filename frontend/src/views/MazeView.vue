<template>
  <div class="maze-view">
    <h1>Maze Navigator</h1>
    <p>Find paths through mazes using BFS, DFS, and A* algorithms</p>

    <div class="puzzle-container">
      <div class="puzzle-board">
        <MazeGrid
          :grid="grid"
          :start="start"
          :end="end"
          :path="path"
          :visited="visited"
          :interactive="true"
          :editMode="editMode"
          @update:grid="grid = $event"
          @update:start="start = $event"
          @update:end="end = $event"
        />

        <div class="button-group">
          <button class="btn-primary" @click="solveMaze" :disabled="isLoading">
            <span class="material-icons">play_arrow</span>
            {{ isLoading ? 'Finding...' : 'Find Path' }}
          </button>
          <button class="btn-secondary" @click="generateMaze">
            <span class="material-icons">auto_awesome</span>
            Generate
          </button>
          <button class="btn-secondary" @click="clearMaze">
            <span class="material-icons">clear</span>
            Clear
          </button>
        </div>
      </div>

      <div class="puzzle-controls">
        <div class="controls-card">
          <h3>Algorithm</h3>
          <select v-model="algorithm" class="select-field">
            <option v-for="algo in algorithms" :key="algo.value" :value="algo.value">
              {{ algo.label }}
            </option>
          </select>
        </div>

        <div class="controls-card">
          <h3>Edit Mode</h3>
          <div class="edit-mode-buttons">
            <button
              @click="editMode = 'wall'"
              :class="['mode-btn', { active: editMode === 'wall' }]"
            >
              Wall
            </button>
            <button
              @click="editMode = 'start'"
              :class="['mode-btn', { active: editMode === 'start' }]"
            >
              Start
            </button>
            <button
              @click="editMode = 'end'"
              :class="['mode-btn', { active: editMode === 'end' }]"
            >
              End
            </button>
          </div>
        </div>

        <div class="controls-card">
          <h3>Maze Size</h3>
          <div class="slider-container">
            <input
              type="range"
              v-model.number="mazeSize"
              min="10"
              max="30"
              step="5"
              class="slider"
            />
            <div class="slider-label">{{ mazeSize }}×{{ mazeSize }}</div>
          </div>
        </div>

        <div class="controls-card">
          <h3>Options</h3>
          <label class="checkbox-container">
            <input type="checkbox" v-model="returnSteps" />
            <span class="checkmark"></span>
            Show exploration steps
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
              <div class="stat-label">NODES</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ statistics.algorithm_used }}</div>
              <div class="stat-label">ALGORITHM</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ path.length }}</div>
              <div class="stat-label">PATH LENGTH</div>
            </div>
          </div>
        </div>

        <div v-if="steps.length > 0" class="steps-card">
          <div class="steps-header">
            <h3>Exploration Steps</h3>
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
        <p>Finding path...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { usePuzzleStore } from '../stores/puzzle'
import { puzzleAPI } from '../services/api'
import { createEmptyGrid, delay, formatTime } from '../utils/helpers'
import MazeGrid from '../components/MazeGrid.vue'

const store = usePuzzleStore()

const grid = ref(createEmptyGrid(15, 15))
const start = ref([0, 0])
const end = ref([14, 14])
const path = ref([])
const visited = ref([])
const steps = ref([])
const statistics = ref(null)
const isLoading = ref(false)
const algorithm = ref('bfs')
const editMode = ref('wall')
const mazeSize = ref(15)
const returnSteps = ref(true)
const animateSolution = ref(true)
const currentStep = ref(0)
const isPlaying = ref(false)
const playInterval = ref(null)

const algorithms = [
  { value: 'bfs', label: 'BFS (Breadth-First)' },
  { value: 'dfs', label: 'DFS (Depth-First)' },
  { value: 'astar', label: 'A* (Heuristic)' }
]

const solveMaze = async () => {
  try {
    isLoading.value = true
    path.value = []
    visited.value = []
    store.setAlgorithm(algorithm.value)
    store.setReturnSteps(returnSteps.value)

    // Ensure start and end are arrays of integers
    const startPos = [parseInt(start.value[0]), parseInt(start.value[1])]
    const endPos = [parseInt(end.value[0]), parseInt(end.value[1])]

    const result = await store.solveMaze(grid.value, startPos, endPos, algorithm.value)

    if (result.success) {
      if (animateSolution.value) {
        await animatePath(result.solution)
      } else {
        path.value = result.solution
      }
      steps.value = result.steps || []
      statistics.value = result.statistics
    } else {
      alert('No path found!')
    }
  } catch (error) {
    console.error('Error solving maze:', error)
    alert('Error solving maze: ' + (error.response?.data?.detail || error.message))
  } finally {
    isLoading.value = false
  }
}

const animatePath = async (solution) => {
  for (const pos of solution) {
    path.value = [...path.value, pos]
    await delay(50)
  }
}

const generateMaze = async () => {
  try {
    // Ensure mazeSize is an integer
    const size = parseInt(mazeSize.value)
    const response = await puzzleAPI.generateMaze(size)
    grid.value = response.data.grid
    start.value = response.data.start
    end.value = response.data.end
    path.value = []
    visited.value = []
    steps.value = []
    statistics.value = null
  } catch (error) {
    console.error('Error generating maze:', error)
    alert('Error generating maze: ' + (error.response?.data?.detail || error.message))
  }
}

const clearMaze = () => {
  const size = parseInt(mazeSize.value)
  grid.value = createEmptyGrid(size, size)
  start.value = [0, 0]
  end.value = [size - 1, size - 1]
  path.value = []
  visited.value = []
  steps.value = []
  statistics.value = null
  currentStep.value = 0
}

const nextStep = () => {
  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++
    const step = steps.value[currentStep.value]
    if (step && step.position) {
      visited.value = [...visited.value, step.position]
    }
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
    if (visited.value.length > 0) {
      visited.value.pop()
    }
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
    }, 100)
  } else {
    clearInterval(playInterval.value)
  }
}

watch(mazeSize, (newSize) => {
  const size = parseInt(newSize)
  grid.value = createEmptyGrid(size, size)
  start.value = [0, 0]
  end.value = [size - 1, size - 1]
  path.value = []
  visited.value = []
  steps.value = []
  statistics.value = null
  currentStep.value = 0
})

onUnmounted(() => {
  if (playInterval.value) {
    clearInterval(playInterval.value)
  }
})
</script>

<style scoped>
.maze-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.maze-view h1 {
  color: #1976d2;
  margin-bottom: 8px;
  font-size: 32px;
}

.maze-view > p {
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
  max-width: 100%;
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

.edit-mode-buttons {
  display: flex;
  gap: 8px;
}

.mode-btn {
  flex: 1;
  padding: 10px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.mode-btn:hover {
  border-color: #4CAF50;
  background: #E8F5E9;
}

.mode-btn.active {
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  color: white;
  border-color: transparent;
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

@media (max-width: 768px) {
  .puzzle-container {
    flex-direction: column;
  }

  .puzzle-controls {
    width: 100%;
  }
}
</style>