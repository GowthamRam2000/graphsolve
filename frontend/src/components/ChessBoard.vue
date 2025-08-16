<template>
  <div class="chessboard-container">
    <div class="chessboard" :style="boardStyle">
      <div v-for="row in size" :key="row" class="board-row">
        <div
          v-for="col in size"
          :key="col"
          :class="getCellClass(row - 1, col - 1)"
          @click="onCellClick(row - 1, col - 1)"
          class="board-cell"
        >
          <div v-if="getPiece(row - 1, col - 1)" class="piece">
            {{ getPiece(row - 1, col - 1) }}
          </div>
          <div v-if="showNumbers && getNumber(row - 1, col - 1) !== null" class="move-number">
            {{ getNumber(row - 1, col - 1) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: Number,
    default: 8
  },
  pieces: {
    type: Array,
    default: () => []
  },
  pieceType: {
    type: String,
    default: 'queen'
  },
  highlighted: {
    type: Array,
    default: () => []
  },
  path: {
    type: Array,
    default: () => []
  },
  showNumbers: {
    type: Boolean,
    default: false
  },
  interactive: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['cellClick'])

const pieceSymbols = {
  queen: '♛',
  knight: '♞',
  king: '♚',
  rook: '♜'
}

const boardStyle = computed(() => {
  // Dynamically calculate cell size based on board size
  const maxBoardSize = 600; // Maximum board width/height in pixels
  const cellSize = Math.floor(maxBoardSize / props.size);
  return {
    '--cell-size': `${cellSize}px`,
    width: `${cellSize * props.size}px`,
    height: `${cellSize * props.size}px`
  }
})

const getCellClass = (row, col) => {
  const classes = ['board-cell']
  const isDark = (row + col) % 2 === 1
  classes.push(isDark ? 'dark' : 'light')

  if (isHighlighted(row, col)) {
    classes.push('highlighted')
  }

  if (props.interactive) {
    classes.push('interactive')
  }

  return classes.join(' ')
}

const isHighlighted = (row, col) => {
  const r = parseInt(row)
  const c = parseInt(col)
  return props.highlighted.some(([hr, hc]) => parseInt(hr) === r && parseInt(hc) === c)
}

const getPiece = (row, col) => {
  const r = parseInt(row)
  const c = parseInt(col)
  const hasPiece = props.pieces.some(([pr, pc]) => parseInt(pr) === r && parseInt(pc) === c)
  return hasPiece ? pieceSymbols[props.pieceType] : null
}

const getNumber = (row, col) => {
  const r = parseInt(row)
  const c = parseInt(col)
  const index = props.path.findIndex(([pr, pc]) => parseInt(pr) === r && parseInt(pc) === c)
  return index >= 0 ? index : null
}

const onCellClick = (row, col) => {
  if (props.interactive) {
    emit('cellClick', [parseInt(row), parseInt(col)])
  }
}
</script>

<style scoped>
.chessboard-container {
  display: inline-block;
  padding: 10px;
}

.chessboard {
  display: inline-block;
  border: 3px solid #333;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.board-row {
  display: flex;
}

.board-cell {
  width: var(--cell-size, 60px);
  height: var(--cell-size, 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  cursor: default;
  transition: all 0.2s;
}

.board-cell.interactive {
  cursor: pointer;
}

.board-cell.interactive:hover {
  opacity: 0.8;
  transform: scale(0.95);
}

.board-cell.light {
  background: #F0D9B5;
}

.board-cell.dark {
  background: #B58863;
}

.board-cell.highlighted {
  background: #FFE082 !important;
}

.piece {
  font-size: calc(var(--cell-size, 60px) * 0.6);
  color: #333;
  user-select: none;
  filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.3));
}

.move-number {
  position: absolute;
  top: 2px;
  right: 4px;
  font-size: calc(var(--cell-size, 60px) * 0.2);
  font-weight: bold;
  color: #666;
  background: rgba(255, 255, 255, 0.9);
  padding: 1px 3px;
  border-radius: 3px;
  line-height: 1;
}

/* Responsive adjustments for smaller boards */
@media (max-width: 768px) {
  .chessboard-container {
    padding: 5px;
  }
}
</style>