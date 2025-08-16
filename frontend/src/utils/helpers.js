export function createEmptySudoku() {
  return Array(9).fill(null).map(() => Array(9).fill(0))
}

export function createEmptyGrid(rows, cols, fillValue = 0) {
  return Array(rows).fill(null).map(() => Array(cols).fill(fillValue))
}

export function isValidSudokuInput(value) {
  const num = parseInt(value)
  return !isNaN(num) && num >= 0 && num <= 9
}

export function formatTime(ms) {
  if (ms < 1) {
    return `${ms.toFixed(2)}ms`
  }
  if (ms < 1000) {
    return `${ms.toFixed(0)}ms`
  }
  return `${(ms / 1000).toFixed(2)}s`
}

export function formatNumber(num) {
  return num.toLocaleString()
}

export function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export function getCellColor(value, isOriginal, isHighlighted) {
  if (isHighlighted) return '#FFE082'
  if (isOriginal) return '#E0E0E0'
  if (value > 0) return '#C8E6C9'
  return '#FFFFFF'
}

export function isValidPosition(pos, gridSize) {
  return pos[0] >= 0 && pos[0] < gridSize && pos[1] >= 0 && pos[1] < gridSize
}

export function getManhattanDistance(pos1, pos2) {
  return Math.abs(pos1[0] - pos2[0]) + Math.abs(pos1[1] - pos2[1])
}

export function deepCopy(obj) {
  return JSON.parse(JSON.stringify(obj))
}