<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <div class="logo" @click="goHome">
          <span class="logo-icon">🧩</span>
          <h1>GraphPuzzle</h1>
        </div>
        <nav class="nav-menu">
          <button class="nav-btn" @click="goTo('/sudoku')" :class="{ active: $route.path === '/sudoku' }">
            Sudoku
          </button>
          <button class="nav-btn" @click="goTo('/nqueens')" :class="{ active: $route.path === '/nqueens' }">
            N-Queens
          </button>
          <button class="nav-btn" @click="goTo('/maze')" :class="{ active: $route.path === '/maze' }">
            Maze
          </button>
          <button class="nav-btn" @click="goTo('/knight')" :class="{ active: $route.path === '/knight' }">
            Knight's Tour
          </button>
        </nav>
      </div>
    </header>
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const goHome = () => router.push('/')
const goTo = (path) => router.push(path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: white;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 32px;
}

.logo h1 {
  background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 28px;
  font-weight: 700;
}

.nav-menu {
  display: flex;
  gap: 8px;
}

.nav-btn {
  padding: 10px 20px;
  border: none;
  background: transparent;
  color: #666;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 24px;
  transition: all 0.3s;
  position: relative;
}

.nav-btn:hover {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.nav-btn.active {
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  color: white;
}

.app-main {
  flex: 1;
  padding: 32px 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>