<script setup lang="ts">
import Container from '@/components/Container.vue';
</script>

<template>
  <Container
    :class="$style.container"
    max-width="400px"
  >
    <router-view />
  </Container>
</template>

<style module lang="scss">
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
