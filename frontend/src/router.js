import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import SudokuView from './views/SudokuView.vue'
import NQueensView from './views/NQueensView.vue'
import MazeView from './views/MazeView.vue'
import KnightView from './views/KnightView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/sudoku',
    name: 'sudoku',
    component: SudokuView
  },
  {
    path: '/nqueens',
    name: 'nqueens',
    component: NQueensView
  },
  {
    path: '/maze',
    name: 'maze',
    component: MazeView
  },
  {
    path: '/knight',
    name: 'knight',
    component: KnightView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router