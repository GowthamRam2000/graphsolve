<template>
  <div class="home-view">
    <div class="hero">
      <h1>GraphPuzzle</h1>
      <p>Explore classic puzzles through the lens of graph theory</p>
    </div>

    <div class="puzzles-grid">
      <div class="puzzle-card" @click="goTo('/sudoku')">
        <div class="puzzle-icon">🔢</div>
        <h2>Sudoku</h2>
        <p>Solve the classic number puzzle using graph coloring algorithms</p>
        <div class="puzzle-info">
          <div class="info-item">
            <span class="material-icons">hub</span>
            <span>Graph Coloring</span>
          </div>
          <div class="info-item">
            <span class="material-icons">speed</span>
            <span>O(9<sup>m</sup>)</span>
          </div>
        </div>
        <button class="solve-btn">Solve Now</button>
      </div>

      <div class="puzzle-card" @click="goTo('/nqueens')">
        <div class="puzzle-icon">♛</div>
        <h2>N-Queens</h2>
        <p>Place queens on a chessboard using constraint satisfaction</p>
        <div class="puzzle-info">
          <div class="info-item">
            <span class="material-icons">account_tree</span>
            <span>CSP</span>
          </div>
          <div class="info-item">
            <span class="material-icons">speed</span>
            <span>O(N!)</span>
          </div>
        </div>
        <button class="solve-btn">Solve Now</button>
      </div>

      <div class="puzzle-card" @click="goTo('/maze')">
        <div class="puzzle-icon">🌀</div>
        <h2>Maze Navigator</h2>
        <p>Find paths through mazes with BFS, DFS, and A* algorithms</p>
        <div class="puzzle-info">
          <div class="info-item">
            <span class="material-icons">route</span>
            <span>Pathfinding</span>
          </div>
          <div class="info-item">
            <span class="material-icons">speed</span>
            <span>O(V+E)</span>
          </div>
        </div>
        <button class="solve-btn">Solve Now</button>
      </div>

      <div class="puzzle-card" @click="goTo('/knight')">
        <div class="puzzle-icon">♞</div>
        <h2>Knight's Tour</h2>
        <p>Navigate a knight across the chessboard visiting each square once</p>
        <div class="puzzle-info">
          <div class="info-item">
            <span class="material-icons">timeline</span>
            <span>Hamiltonian Path</span>
          </div>
          <div class="info-item">
            <span class="material-icons">speed</span>
            <span>O(8<sup>N</sup>)</span>
          </div>
        </div>
        <button class="solve-btn">Solve Now</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

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
  padding: 48px 24px;
  background: linear-gradient(135deg, #E8F5E9 0%, #E3F2FD 100%);
  border-radius: 16px;
  margin-bottom: 48px;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero p {
  font-size: 20px;
  color: #666;
}

.puzzles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.puzzle-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border: 2px solid transparent;
}

.puzzle-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  border-color: #4CAF50;
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
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: 100%;
  max-width: 200px;
}

.solve-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
}
</style>