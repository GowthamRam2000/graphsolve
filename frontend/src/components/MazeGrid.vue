<template>
  <div class="maze-container">
    <div class="maze-grid" :style="gridStyle">
      <div
        v-for="(row, i) in grid"
        :key="i"
        class="maze-row"
      >
        <div
          v-for="(cell, j) in row"
          :key="j"
          :class="getCellClass(i, j)"
          @click="onCellClick(i, j)"
          class="maze-cell"
        >
          <span v-if="isStart(i, j)" class="cell-marker">S</span>
          <span v-else-if="isEnd(i, j)" class="cell-marker">E</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  grid: {
    type: Array,
    required: true
  },
  start: {
    type: Array,
    default: () => [0, 0]
  },
  end: {
    type: Array,
    default: () => [0, 0]
  },
  path: {
    type: Array,
    default: () => []
  },
  visited: {
    type: Array,
    default: () => []
  },
  interactive: {
    type: Boolean,
    default: false
  },
  editMode: {
    type: String,
    default: 'wall' // 'wall', 'start', 'end'
  }
})

const emit = defineEmits(['cellClick', 'update:grid', 'update:start', 'update:end'])

const gridStyle = computed(() => {
  if (!props.grid || !props.grid[0]) return {}

  const rows = props.grid.length
  const cols = props.grid[0].length
  const maxSize = 600 // Maximum grid size in pixels

  // Calculate cell size to fit within max size
  const cellSize = Math.min(
    Math.floor(maxSize / Math.max(rows, cols)),
    30 // Maximum cell size
  )

  return {
    '--cell-size': `${cellSize}px`,
    '--grid-cols': cols,
    '--grid-rows': rows,
    width: `${cellSize * cols}px`,
    height: `${cellSize * rows}px`
  }
})

const getCellClass = (row, col) => {
  const classes = []

  if (props.grid[row][col] === 1) {
    classes.push('wall')
  } else {
    classes.push('path')
  }

  if (isInPath(row, col)) {
    classes.push('solution-path')
  } else if (isVisited(row, col)) {
    classes.push('visited')
  }

  if (isStart(row, col)) {
    classes.push('start')
  } else if (isEnd(row, col)) {
    classes.push('end')
  }

  if (props.interactive) {
    classes.push('interactive')
  }

  return classes.join(' ')
}

const isStart = (row, col) => {
  return parseInt(props.start[0]) === parseInt(row) && parseInt(props.start[1]) === parseInt(col)
}

const isEnd = (row, col) => {
  return parseInt(props.end[0]) === parseInt(row) && parseInt(props.end[1]) === parseInt(col)
}

const isInPath = (row, col) => {
  const r = parseInt(row)
  const c = parseInt(col)
  return props.path.some(([pr, pc]) => parseInt(pr) === r && parseInt(pc) === c)
}

const isVisited = (row, col) => {
  const r = parseInt(row)
  const c = parseInt(col)
  return props.visited.some(([vr, vc]) => parseInt(vr) === r && parseInt(vc) === c)
}

const onCellClick = (row, col) => {
  if (!props.interactive) return

  // Ensure row and col are integers
  const r = parseInt(row)
  const c = parseInt(col)

  if (props.editMode === 'start') {
    emit('update:start', [r, c])
  } else if (props.editMode === 'end') {
    emit('update:end', [r, c])
  } else if (props.editMode === 'wall') {
    const newGrid = props.grid.map(row => [...row])
    newGrid[r][c] = newGrid[r][c] === 0 ? 1 : 0
    emit('update:grid', newGrid)
  }

  emit('cellClick', [r, c])
}
</script>

<style scoped>
.maze-container {
  display: inline-block;
  padding: 10px;
}

.maze-grid {
  display: inline-block;
  border: 3px solid var(--on-surface);
  background: var(--surface);
  box-shadow: var(--shadow-lg);
  border-radius: var(--radius-md);
  overflow: hidden;
  position: relative;
}

.maze-grid::before {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent), var(--primary));
  background-size: 400% 400%;
  border-radius: var(--radius-md);
  z-index: -1;
  animation: gradientShift 8s ease infinite;
  opacity: 0.1;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.maze-row {
  display: flex;
}

.maze-cell {
  width: var(--cell-size, 20px);
  height: var(--cell-size, 20px);
  border: 0.5px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  position: relative;
}

.cell-marker {
  font-size: calc(var(--cell-size, 20px) * 0.6);
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.maze-cell.wall {
  background: #333;
}

.maze-cell.path {
  background: white;
}

.maze-cell.visited {
  background: #E1F5FE;
  animation: visitedPulse 0.3s ease-out;
}

.maze-cell.solution-path {
  background: var(--success);
  animation: pathPulse 0.4s ease-out;
  box-shadow: 0 0 8px rgba(46, 125, 50, 0.4);
}

.maze-cell.start {
  background: var(--secondary) !important;
  color: var(--on-secondary);
  box-shadow: 0 0 12px rgba(13, 71, 161, 0.5);
}

.maze-cell.end {
  background: var(--accent) !important;
  color: var(--on-accent);
  box-shadow: 0 0 12px rgba(255, 111, 0, 0.5);
}

.maze-cell.interactive {
  cursor: pointer;
}

.maze-cell.interactive:hover {
  opacity: 0.7;
  transform: scale(0.9);
}

@keyframes visitedPulse {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes pathPulse {
  0% {
    transform: scale(0.8);
    background: #81C784;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    background: #4CAF50;
  }
}
</style>