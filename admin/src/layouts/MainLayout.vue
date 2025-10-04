<script setup lang="ts">
import Container from '@/components/Container.vue';
import Header from '@/components/Header.vue';
</script>

<template>
  <Header />
  <Container>
    <router-view />
  </Container>
</template>
