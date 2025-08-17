import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const puzzleAPI = {
  solveSudoku(grid, options = {}) {
    return api.post('/sudoku/solve', {
      puzzle_type: 'sudoku',
      input: { grid },
      options
    })
  },

  solveNQueens(n, presetQueens = [], options = {}) {
    return api.post('/nqueens/solve', {
      puzzle_type: 'nqueens',
      input: { n, preset_queens: presetQueens },
      options
    })
  },

  solveMaze(grid, start, end, options = {}) {
    return api.post('/maze/solve', {
      puzzle_type: 'maze',
      input: { grid, start, end },
      options
    })
  },

  solveKnight(n, start, closedTour = false, options = {}) {
    return api.post('/knight/solve', {
      puzzle_type: 'knight',
      input: {
        n: parseInt(n),
        start: [parseInt(start[0]), parseInt(start[1])],
        closed_tour: closedTour
      },
      options
    })
  },

  getPresets(puzzleType) {
    return api.get(`/puzzles/presets/${puzzleType}`)
  },

  getAlgorithms(puzzleType) {
    return api.get(`/puzzles/algorithms/${puzzleType}`)
  },

  generateMaze(size = 10, difficulty = 'medium') {
    return api.post('/maze/generate', {
      size: parseInt(size),
      difficulty
    })
  },

  checkHealth() {
    return api.get('/health')
  }
}

export
default api