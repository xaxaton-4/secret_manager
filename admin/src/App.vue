<script setup lang="ts">
import ConfirmPopup from 'primevue/confirmpopup';
import Toast from 'primevue/toast';
import { useAuthStore } from './store/auth';

const authStore = useAuthStore();
</script>

<template>
  <router-view v-if="authStore.isReady" />
  <Toast />
  <ConfirmPopup />
</template>
