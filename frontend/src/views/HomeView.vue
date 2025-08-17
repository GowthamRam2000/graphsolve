<template>
  <div class="home-view">
    <div class="hero">
      <h1>GraphPuzzle</h1>
      <p>Explore classic puzzles through the lens of graph theory</p>
    </div>

    <div class="puzzles-grid">
      <div class="puzzle-card" @click="goTo('/sudoku')">
        <div class="puzzle-icon">
          <IconSystem name="sudoku" :size="64" color="var(--primary)" />
        </div>
        <h2>Sudoku</h2>
        <p>Solve the classic number puzzle using graph coloring algorithms</p>
        <div class="puzzle-info">
          <div class="info-item">
            <IconSystem name="graph" :size="18" color="var(--primary)" />
            <span>Graph Coloring</span>
          </div>
          <div class="info-item">
            <IconSystem name="speed" :size="18" color="var(--primary)" />
            <span>O(9<sup>m</sup>)</span>
          </div>
        </div>
        <button class="solve-btn">
          <IconSystem name="play" :size="16" />
          Solve Now
        </button>
      </div>

      <div class="puzzle-card" @click="goTo('/nqueens')">
        <div class="puzzle-icon">
          <IconSystem name="chess-queen" :size="64" color="var(--secondary)" />
        </div>
        <h2>N-Queens</h2>
        <p>Place queens on a chessboard using constraint satisfaction</p>
        <div class="puzzle-info">
          <div class="info-item">
            <IconSystem name="algorithm" :size="18" color="var(--secondary)" />
            <span>CSP</span>
          </div>
          <div class="info-item">
            <IconSystem name="speed" :size="18" color="var(--secondary)" />
            <span>O(N!)</span>
          </div>
        </div>
        <button class="solve-btn">
          <IconSystem name="play" :size="16" />
          Solve Now
        </button>
      </div>

      <div class="puzzle-card" @click="goTo('/maze')">
        <div class="puzzle-icon">
          <IconSystem name="maze" :size="64" color="var(--accent)" />
        </div>
        <h2>Maze Navigator</h2>
        <p>Find paths through mazes with BFS, DFS, and A* algorithms</p>
        <div class="puzzle-info">
          <div class="info-item">
            <IconSystem name="algorithm" :size="18" color="var(--accent)" />
            <span>Pathfinding</span>
          </div>
          <div class="info-item">
            <IconSystem name="speed" :size="18" color="var(--accent)" />
            <span>O(V+E)</span>
          </div>
        </div>
        <button class="solve-btn">
          <IconSystem name="play" :size="16" />
          Solve Now
        </button>
      </div>

      <div class="puzzle-card" @click="goTo('/knight')">
        <div class="puzzle-icon">
          <IconSystem name="chess-knight" :size="64" color="var(--primary-light)" />
        </div>
        <h2>Knight's Tour</h2>
        <p>Navigate a knight across the chessboard visiting each square once</p>
        <div class="puzzle-info">
          <div class="info-item">
            <IconSystem name="algorithm" :size="18" color="var(--primary-light)" />
            <span>Hamiltonian Path</span>
          </div>
          <div class="info-item">
            <IconSystem name="speed" :size="18" color="var(--primary-light)" />
            <span>O(8<sup>N</sup>)</span>
          </div>
        </div>
        <button class="solve-btn">
          <IconSystem name="play" :size="16" />
          Solve Now
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import IconSystem from '../components/IconSystem.vue'

const router = useRouter()

const goTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.hero {
  text-align: center;
  padding: 64px 32px;
  background: linear-gradient(135deg, var(--primary-surface) 0%, var(--secondary-surface) 100%);
  border-radius: var(--radius-2xl);
  margin-bottom: 48px;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.hero h1 {
  font-size: var(--font-size-5xl);
  margin-bottom: 24px;
  font-weight: var(--font-weight-extrabold);
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary-light) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
  line-height: var(--line-height-tight);
}

.hero p {
  font-size: var(--font-size-xl);
  color: var(--on-surface-variant);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-relaxed);
}

.puzzles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.puzzle-card {
  background: var(--surface);
  border-radius: var(--radius-xl);
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.puzzle-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left var(--transition-slow);
}

.puzzle-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: var(--shadow-xl);
  border-color: var(--primary);
}

.puzzle-card:hover::before {
  left: 100%;
}

.puzzle-icon {
  font-size: 64px;
  margin-bottom: 16px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.puzzle-card h2 {
  font-size: 24px;
  margin-bottom: 12px;
  color: #333;
}

.puzzle-card p {
  color: #666;
  margin-bottom: 20px;
  min-height: 48px;
  font-size: 14px;
  line-height: 1.5;
}

.puzzle-info {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 24px;
  padding: 16px;
  background: #F5F5F5;
  border-radius: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #555;
}

.info-item .material-icons {
  font-size: 18px;
  color: #4CAF50;
}

.info-item span sup {
  font-size: 10px;
  vertical-align: super;
}

.solve-btn {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: var(--on-primary);
  border: none;
  padding: 14px 32px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-bounce);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: 100%;
  max-width: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.solve-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.solve-btn:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: var(--shadow-primary);
}

.solve-btn:active::before {
  width: 300px;
  height: 300px;
}
</style>