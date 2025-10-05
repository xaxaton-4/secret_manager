<script setup lang="ts">
import { watch } from 'vue';
import ConfirmPopup from 'primevue/confirmpopup';
import Toast from 'primevue/toast';
import { useSocket } from '@/composables/socket';
import { useAuthStore } from './store/auth';

const authStore = useAuthStore();
const { initSocket } = useSocket();

watch([() => authStore.isAuth, () => authStore.isReady], (isAuth, isReady) => {
  if (isAuth && isReady) {
    initSocket();
  }
});
</script>

<template>
  <router-view v-if="authStore.isReady" />
  <Toast />
  <ConfirmPopup />
</template>
