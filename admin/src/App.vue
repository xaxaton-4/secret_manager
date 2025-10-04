<script setup lang="ts">
import ConfirmPopup from 'primevue/confirmpopup';
import Toast from 'primevue/toast';
</script>

<template>
  <router-view />
  <Toast />
  <ConfirmPopup />
</template>
