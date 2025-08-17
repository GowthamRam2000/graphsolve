<template>
  <div class="sudoku-grid-container">
    <div class="sudoku-grid" :class="{ 'solving': isAnimating }">
      <div v-for="(row, i) in displayGrid" :key="i" class="sudoku-row">
        <div
          v-for="(cell, j) in row"
          :key="j"
          :class="getCellClass(i, j)"
          class="sudoku-cell"
        >
          <input
            type="text"
            :value="cell === 0 ? '' : cell"
            @input="onCellInput(i, j, $event)"
            :disabled="isOriginal[i][j] || disabled"
            :class="{
              'original': isOriginal[i][j],
              'solution': isSolutionCell(i, j),
              'animating': animatingCell?.row === i && animatingCell?.col === j,
              'highlighted': highlightedCells.has(`${i}-${j}`)
            }"
            maxlength="1"
          />
          <div v-if="animatingCell?.row === i && animatingCell?.col === j" class="pulse-ring"></div>
        </div>
      </div>
    </div>

    <!-- 3D Visualization Overlay -->
    <transition name="fade">
      <div v-if="showVisualization" class="visualization-overlay">
        <div class="graph-nodes">
          <div v-for="node in graphNodes" :key="node.id"
               class="graph-node"
               :style="{ left: node.x + 'px', top: node.y + 'px' }">
            {{ node.value }}
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { isValidSudokuInput, delay } from '../utils/helpers'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => Array(9).fill(null).map(() => Array(9).fill(0))
  },
  solution: Array,
  disabled: Boolean,
  originalCells: Array,
  animationSteps: Array,
  isAnimating: Boolean
})

const emit = defineEmits(['update:modelValue', 'animationComplete'])

const grid = ref(props.modelValue)
const displayGrid = ref(props.modelValue)
const isOriginal = ref(props.originalCells || Array(9).fill(null).map(() => Array(9).fill(false)))
const animatingCell = ref(null)
const highlightedCells = ref(new Set())
const showVisualization = ref(false)
const graphNodes = ref([])

watch(() => props.modelValue, (newVal) => {
  grid.value = newVal
  displayGrid.value = newVal
})

watch(() => props.originalCells, (newVal) => {
  if (newVal) {
    isOriginal.value = newVal
  }
})

watch(() => props.solution, async (newSolution) => {
  if (newSolution && props.isAnimating) {
    await animateSolution(newSolution)
  } else if (newSolution) {
    displayGrid.value = newSolution
  }
})

const animateSolution = async (solution) => {
  const steps = []

  // Find differences between current grid and solution
  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      if (grid.value[i][j] === 0 && solution[i][j] !== 0) {
        steps.push({ row: i, col: j, value: solution[i][j] })
      }
    }
  }

  // Animate each step
  for (const step of steps) {
    animatingCell.value = step
    highlightRelatedCells(step.row, step.col)

    await delay(150)

    const newGrid = [...displayGrid.value]
    newGrid[step.row] = [...newGrid[step.row]]
    newGrid[step.row][step.col] = step.value
    displayGrid.value = newGrid

    await delay(100)
    animatingCell.value = null
    highlightedCells.value.clear()
  }

  emit('animationComplete')
}

const highlightRelatedCells = (row, col) => {
  highlightedCells.value.clear()

  // Highlight row
  for (let j = 0; j < 9; j++) {
    if (j !== col) highlightedCells.value.add(`${row}-${j}`)
  }

  // Highlight column
  for (let i = 0; i < 9; i++) {
    if (i !== row) highlightedCells.value.add(`${i}-${col}`)
  }

  // Highlight 3x3 box
  const boxRow = Math.floor(row / 3) * 3
  const boxCol = Math.floor(col / 3) * 3
  for (let i = boxRow; i < boxRow + 3; i++) {
    for (let j = boxCol; j < boxCol + 3; j++) {
      if (i !== row || j !== col) {
        highlightedCells.value.add(`${i}-${j}`)
      }
    }
  }
}

const onCellInput = (row, col, event) => {
  const value = event.target.value
  if (value === '' || isValidSudokuInput(value)) {
    const newGrid = [...grid.value]
    newGrid[row] = [...newGrid[row]]
    newGrid[row][col] = value === '' ? 0 : parseInt(value)
    grid.value = newGrid
    displayGrid.value = newGrid
    emit('update:modelValue', newGrid)
  } else {
    event.target.value = grid.value[row][col] === 0 ? '' : grid.value[row][col]
  }
}

const getCellClass = (row, col) => {
  const classes = []
  if (col % 3 === 2 && col < 8) classes.push('border-right')
  if (row % 3 === 2 && row < 8) classes.push('border-bottom')
  return classes.join(' ')
}

const isSolutionCell = (row, col) => {
  return props.solution &&
         props.solution[row][col] !== grid.value[row][col] &&
         !isOriginal.value[row][col]
}
</script>

<style scoped>
.sudoku-grid-container {
  position: relative;
  display: inline-block;
}

.sudoku-grid {
  display: inline-block;
  border: 3px solid var(--secondary);
  background: var(--surface);
  padding: 6px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-normal);
  position: relative;
}

.sudoku-grid::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent));
  border-radius: var(--radius-lg);
  z-index: -1;
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.sudoku-grid:hover::before {
  opacity: 0.1;
}

.sudoku-grid.solving {
  transform: scale(1.02);
}

.sudoku-row {
  display: flex;
}

.sudoku-cell {
  width: 55px;
  height: 55px;
  position: relative;
}

.sudoku-cell input {
  width: 100%;
  height: 100%;
  border: 1px solid #e0e0e0;
  text-align: center;
  font-size: 22px;
  font-weight: 500;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  color: #333;
}

.sudoku-cell input:focus {
  background: var(--secondary-surface);
  border-color: var(--secondary);
  box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.2);
  transform: scale(1.08);
  z-index: 10;
  position: relative;
}

.sudoku-cell input.original {
  background: #ECEFF1;
  font-weight: 700;
  color: #263238;
}

.sudoku-cell input.solution {
  color: var(--success);
  font-weight: var(--font-weight-semibold);
  animation: solutionPulse 0.6s ease-out;
}

.sudoku-cell input.animating {
  background: linear-gradient(45deg, var(--success), var(--success-light));
  color: var(--on-success);
  transform: scale(1.12);
  box-shadow: var(--shadow-primary);
  z-index: 20;
  font-weight: var(--font-weight-bold);
}

.sudoku-cell input.highlighted {
  background: rgba(255, 235, 59, 0.2);
}

.sudoku-cell input:disabled {
  cursor: not-allowed;
}

.border-right {
  border-right: 3px solid #1976d2;
}

.border-bottom {
  border-bottom: 3px solid #1976d2;
}

.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border: 3px solid #4CAF50;
  border-radius: 4px;
  animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1);
  pointer-events: none;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 1;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0.5;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
}

@keyframes solutionPulse {
  0% {
    transform: scale(1);
    background: white;
  }
  50% {
    transform: scale(1.15);
    background: #E8F5E9;
  }
  100% {
    transform: scale(1);
    background: white;
  }
}

.visualization-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 30;
}

.graph-nodes {
  position: relative;
  width: 100%;
  height: 100%;
}

.graph-node {
  position: absolute;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  animation: nodeFloat 3s ease-in-out infinite;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

@keyframes nodeFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>