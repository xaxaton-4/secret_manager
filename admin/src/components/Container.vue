<script setup lang="ts">
defineProps<{
  maxWidth?: string;
}>();
</script>

<template>
  <div
    :class="$style.container"
    :style="{ maxWidth }"
  >
    <slot />
  </div>
</template>

<style module lang="scss">
.container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 0 1rem;
}
</style>
