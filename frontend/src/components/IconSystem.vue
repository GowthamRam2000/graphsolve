<template>
  <span :class="iconClass" :style="iconStyle" v-html="iconSvg"></span>
</template>

<script setup>
import { computed } from 'vue'
//comment
const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [String, Number],
    default: 24
  },
  color: {
    type: String,
    default: 'currentColor'
  },
  variant: {
    type: String,
    default: 'outline',
    validator: (value) => ['outline', 'filled', 'duotone'].includes(value)
  }
})

const iconClass = computed(() => {
  return [
    'icon',
    `icon-${props.variant}`,
    `icon-${props.name}`
  ]
})

const iconStyle = computed(() => {
  return {
    width: typeof props.size === 'number' ? `${props.size}px` : props.size,
    height: typeof props.size === 'number' ? `${props.size}px` : props.size,
    color: props.color,
    display: 'inline-block'
  }
})

const iconSvg = computed(() => {
  const icons = {
    'puzzle': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <path d="M19.439 15.439c0 0-1.439-1.439-2.439-1.439s-2.439 1.439-2.439 1.439V17c0 1.1-.9 2-2 2s-2-.9-2-2v-1.561s-1.439-1.439-2.439-1.439-2.439 1.439-2.439 1.439H5c-1.1 0-2-.9-2-2s.9-2 2-2h1.561c0 0 1.439-1.439 1.439-2.439S6.561 6.561 6.561 6.561V5c0-1.1.9-2 2-2s2 .9 2 2v1.561c0 0 1.439 1.439 2.439 1.439s2.439-1.439 2.439-1.439H17c1.1 0 2 .9 2 2s-.9 2-2 2h-1.561c0 0-1.439 1.439-1.439 2.439s1.439 2.439 1.439 2.439H17c1.1 0 2 .9 2 2s-.9 2-2 2h-1.561z"/>
      </svg>
    `,
    'graph': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <ellipse cx="12" cy="5" rx="3" ry="3"/>
        <ellipse cx="12" cy="19" rx="3" ry="3"/>
        <ellipse cx="5" cy="12" rx="3" ry="3"/>
        <ellipse cx="19" cy="12" rx="3" ry="3"/>
        <line x1="12" y1="8" x2="12" y2="16"/>
        <line x1="8" y1="12" x2="16" y2="12"/>
        <line x1="9.17" y1="7.17" x2="6.83" y2="9.83"/>
        <line x1="14.83" y1="7.17" x2="17.17" y2="9.83"/>
        <line x1="9.17" y1="16.83" x2="6.83" y2="14.17"/>
        <line x1="14.83" y1="16.83" x2="17.17" y2="14.17"/>
      </svg>
    `,
    'algorithm': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        <polyline points="7.5,8 12,11 16.5,8"/>
        <polyline points="7.5,16 12,13 16.5,16"/>
        <line x1="12" y1="11" x2="12" y2="13"/>
      </svg>
    `,
    'chess-queen': `
      <svg viewBox="0 0 24 24" fill="currentColor" style="width: 100%; height: 100%;">
        <path d="M12 2L10 5L8 2L6 5L4 2L2 6L4 8L6 12L8 16L10 18L12 20L14 18L16 16L18 12L20 8L22 6L20 2L18 5L16 2L14 5L12 2Z"/>
        <rect x="6" y="18" width="12" height="2" rx="1"/>
      </svg>
    `,
    'chess-knight': `
      <svg viewBox="0 0 24 24" fill="currentColor" style="width: 100%; height: 100%;">
        <path d="M8 2C7 2 6 3 6 4V6C6 7 7 8 8 8H9L10 9V11H8C7 11 6 12 6 13V15C6 16 7 17 8 17H16C17 17 18 16 18 15V13C18 12 17 11 16 11H14V9C14 8 13 7 12 7H11L10 6H12C13 6 14 5 14 4V3C14 2.5 13.5 2 13 2H12L11 3H10L9 2H8Z"/>
        <rect x="6" y="17" width="12" height="2" rx="1"/>
      </svg>
    `,
    'maze': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
        <path d="M7 7h3v3H7zM14 7h3v3h-3zM7 14h3v3H7z"/>
        <path d="M5 5L12 12M12 12L19 19M12 12L5 19M12 12L19 5" stroke-width="1" opacity="0.3"/>
      </svg>
    `,
    'sudoku': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <rect x="3" y="3" width="18" height="18" rx="1"/>
        <line x1="9" y1="3" x2="9" y2="21"/>
        <line x1="15" y1="3" x2="15" y2="21"/>
        <line x1="3" y1="9" x2="21" y2="9"/>
        <line x1="3" y1="15" x2="21" y2="15"/>
        <circle cx="6" cy="6" r="1" fill="currentColor"/>
        <circle cx="12" cy="6" r="1" fill="currentColor"/>
        <circle cx="18" cy="12" r="1" fill="currentColor"/>
        <circle cx="6" cy="18" r="1" fill="currentColor"/>
      </svg>
    `,
    'play': `
      <svg viewBox="0 0 24 24" fill="currentColor" style="width: 100%; height: 100%;">
        <polygon points="5,3 19,12 5,21"/>
      </svg>
    `,
    'pause': `
      <svg viewBox="0 0 24 24" fill="currentColor" style="width: 100%; height: 100%;">
        <rect x="6" y="4" width="4" height="16"/>
        <rect x="14" y="4" width="4" height="16"/>
      </svg>
    `,
    'reset': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <polyline points="1,4 1,10 7,10"/>
        <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
      </svg>
    `,
    'settings': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
      </svg>
    `,
    'speed': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
      </svg>
    `,
    'time': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12,6 12,12 16,14"/>
      </svg>
    `,
    'check': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <polyline points="20,6 9,17 4,12"/>
      </svg>
    `,
    'close': `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 100%; height: 100%;">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    `
  }

  return icons[props.name] || '<div style="width: 100%; height: 100%; background: #ddd;"></div>'
})
</script>

<style scoped>
.icon {
  display: inline-block;
  vertical-align: middle;
  transition: all var(--transition-fast);
}

.icon-outline {
  fill: none;
  stroke: currentColor;
}

.icon-filled {
  fill: currentColor;
  stroke: none;
}

.icon-duotone {
  fill: currentColor;
  stroke: currentColor;
  opacity: 0.7;
}

.icon:hover {
  transform: scale(1.1);
}
</style>
