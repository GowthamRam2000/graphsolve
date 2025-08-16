<template>
  <div class="difficulty-selector">
    <label>{{ label }}</label>
    <div class="difficulty-buttons">
      <md-outlined-button
        v-for="level in levels"
        :key="level.value"
        @click="selectLevel(level.value)"
        :class="{ active: selected === level.value }"
      >
        {{ level.label }}
      </md-outlined-button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: String,
  label: {
    type: String,
    default: 'Difficulty'
  },
  levels: {
    type: Array,
    default: () => [
      { value: 'easy', label: 'Easy' },
      { value: 'medium', label: 'Medium' },
      { value: 'hard', label: 'Hard' }
    ]
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const selected = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  selected.value = newVal
})

const selectLevel = (value) => {
  selected.value = value
  emit('update:modelValue', value)
  emit('select', value)
}
</script>

<style scoped>
.difficulty-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.difficulty-selector label {
  font-size: 14px;
  color: var(--md-sys-color-on-surface-variant);
}

.difficulty-buttons {
  display: flex;
  gap: 8px;
}

md-outlined-button {
  flex: 1;
}

md-outlined-button.active {
  background: var(--md-sys-color-primary-container);
}
</style>