<script setup lang="ts">
import { Button, Card, ProgressSpinner } from 'primevue';
import { useSecretsStore } from '@/store/secrets';

defineProps<{
  resource: string;
}>();

const secretsStore = useSecretsStore();
</script>

<template>
  <Card>
    <template #content>
      <div :class="$style.content">
        <Button
          v-tooltip.top="'Показать'"
          icon="pi pi-eye"
          aria-label="Показать"
          severity="secondary"
          @click="secretsStore.getSecret(resource)"
        />

        <ProgressSpinner
          v-if="secretsStore.secretsLoading[resource]"
          :class="$style.progress"
        />

        <p v-else>{{ resource }}</p>
      </div>
    </template>
  </Card>
</template>

<style module lang="scss">
.content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress {
  margin: 0 !important;
  width: 30px !important;
  height: 30px !important;
}
</style>
