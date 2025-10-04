<script setup lang="ts">
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

const links = [
  {
    to: '/',
    label: 'Заявки',
  },
  {
    to: '/secrets/new',
    label: 'Новый секрет',
  },
  {
    to: '/dashboard',
    label: 'Дашборд',
  },
];
</script>

<template>
  <header :class="$style.header">
    <router-link
      v-for="link in links"
      :key="link.to"
      :to="link.to"
      :class="$style.link"
    >
      {{ link.label }}
    </router-link>

    <i
      :class="$style.logout"
      class="pi pi-sign-out"
      v-tooltip="'Выйти'"
      @click="authStore.logout"
    />
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

.link {
  position: relative;

  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background-color: var(--p-primary-contrast-color);
    transform: translateY(-0.5rem);
    opacity: 0;
    transition: 0.3s;
  }

  &:global(.router-link-exact-active) {
    &::before {
      transform: translateY(0);
      opacity: 1;
    }
  }
}

.logout {
  margin-left: auto;
  cursor: pointer;
}
</style>
