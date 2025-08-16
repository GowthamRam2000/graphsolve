<template>
  <div class="algorithm-selector">
    <label>Algorithm</label>
    <md-outlined-select v-model="selected" @change="onChange">
      <md-select-option v-for="algo in algorithms" :key="algo.value" :value="algo.value">
        <div slot="headline">{{ algo.label }}</div>
      </md-select-option>
    </md-outlined-select>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: String,
  algorithms: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const selected = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  selected.value = newVal
})

const onChange = () => {
  emit('update:modelValue', selected.value)
}
</script>

<style scoped>
.algorithm-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.algorithm-selector label {
  font-size: 14px;
  color: var(--md-sys-color-on-surface-variant);
}

md-outlined-select {
  width: 100%;
}
</style>