import { defineStore } from 'pinia'
import { puzzleAPI } from '../services/api'

export const usePuzzleStore = defineStore('puzzle', {
  state: () => ({
    currentPuzzle: null,
    solution: null,
    steps: [],
    statistics: null,
    isLoading: false,
    error: null,
    selectedAlgorithm: 'backtracking',
    returnSteps: true,
    animationSpeed: 500
  }),

  actions: {
    async solveSudoku(grid, algorithm = 'backtracking') {
      this.isLoading = true
      this.error = null
      try {
        const response = await puzzleAPI.solveSudoku(grid, {
          algorithm,
          return_steps: this.returnSteps
        })
        this.solution = response.data.solution
        this.steps = response.data.steps || []
        this.statistics = response.data.statistics
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to solve puzzle'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async solveNQueens(n, presetQueens = [], maxSolutions = 1) {
      this.isLoading = true
      this.error = null
      try {
        const response = await puzzleAPI.solveNQueens(n, presetQueens, {
          return_steps: this.returnSteps,
          max_solutions: maxSolutions
        })
        this.solution = response.data.solution
        this.steps = response.data.steps || []
        this.statistics = response.data.statistics
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to solve puzzle'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async solveMaze(grid, start, end, algorithm = 'bfs') {
      this.isLoading = true
      this.error = null
      try {
        const response = await puzzleAPI.solveMaze(grid, start, end, {
          algorithm,
          return_steps: this.returnSteps
        })
        this.solution = response.data.solution
        this.steps = response.data.steps || []
        this.statistics = response.data.statistics
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to solve puzzle'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async solveKnight(n, start, closedTour = false, algorithm = 'warnsdorff') {
      this.isLoading = true
      this.error = null
      try {
        const response = await puzzleAPI.solveKnight(n, start, closedTour, {
          algorithm,
          return_steps: this.returnSteps
        })
        this.solution = response.data.solution
        this.steps = response.data.steps || []
        this.statistics = response.data.statistics
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to solve puzzle'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    clearSolution() {
      this.solution = null
      this.steps = []
      this.statistics = null
      this.error = null
    },

    setAlgorithm(algorithm) {
      this.selectedAlgorithm = algorithm
    },

    setReturnSteps(value) {
      this.returnSteps = value
    },

    setAnimationSpeed(speed) {
      this.animationSpeed = speed
    }
  }
})