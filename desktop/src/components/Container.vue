<script setup lang="ts"></script>

<template>
  <div :class="$style.container">
    <slot />
  </div>
</template>

<style module lang="scss">
.container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
}
</style>
