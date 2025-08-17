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
  background: var(--background-alt);
  min-height: 100vh;
  color: var(--on-background);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--surface);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow-md);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
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
  filter: drop-shadow(var(--shadow-primary));
}

.logo-icon {
  font-size: 32px;
}

.logo h1 {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary-light) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  letter-spacing: -0.5px;
}

.nav-menu {
  display: flex;
  gap: 8px;
}

.nav-btn {
  padding: 12px 24px;
  border: none;
  background: transparent;
  color: var(--on-surface-variant);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  border-radius: var(--radius-full);
  transition: all var(--transition-normal);
  position: relative;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.nav-btn:hover {
  background: var(--primary-surface);
  color: var(--primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.nav-btn.active {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: var(--on-primary);
  box-shadow: var(--shadow-primary);
  transform: translateY(-1px);
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