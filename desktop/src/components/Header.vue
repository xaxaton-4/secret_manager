<script setup lang="ts">
const links = [
  {
    to: '/',
    label: 'Секреты',
  },
  {
    to: '/secrets/new',
    label: 'Новый секрет',
  },
];
</script>

<template>
  <header :class="$style.header">
    <router-link
      v-for="link in links"
      :key="link.to"
      :to="link.to"
    >
      {{ link.label }}
    </router-link>
  </header>
</template>

<style module lang="scss">
.header {
  color: var(--p-primary-contrast-color);
  background-color: var(--p-primary-color);
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
}
</style>
