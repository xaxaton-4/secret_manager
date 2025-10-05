<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { debounce } from 'lodash-es';
import { Card, Button, Skeleton, useToast } from 'primevue';
import { decryptAES } from '@/utils/crypt';

const props = defineProps<{
  resource: string;
  value: string;
  encryptionKey: string;
}>();

const toast = useToast();

const isVisible = ref(false);

const tooltip = computed(() => (isVisible.value ? 'Скрыть' : 'Показать'));

const decrypted = computed(() => decryptAES(props.value, props.encryptionKey));

const onCopy = () => {
  navigator.clipboard.writeText(decrypted.value).then(() => {
    toast.add({
      severity: 'success',
      summary: 'Секрет скопирован в буфер обмена',
      life: 3000,
    });
  });
};

const hideSecret = () => {
  if (isVisible.value) {
    isVisible.value = false;
    toast.add({
      severity: 'info',
      summary: 'Секрет скрыт',
      life: 3000,
    });
  }
};

const debouncedHideSecret = debounce(hideSecret, 3000);

watch(isVisible, () => {
  debouncedHideSecret();
});
</script>

<template>
  <Card>
    <template #title>{{ resource }}</template>

    <template #content>
      <div :class="$style.content">
        <template v-if="decrypted">
          <Button
            v-tooltip.top="tooltip"
            :icon="`pi pi-${isVisible ? 'eye-slash' : 'eye'}`"
            :aria-label="tooltip"
            severity="secondary"
            @click="isVisible = !isVisible"
          />

          <p :class="$style.text">
            {{ decrypted }}

            <Skeleton v-if="!isVisible" />

            <i
              :class="$style.copy"
              class="pi pi-copy"
              v-tooltip.top="'Скопировать'"
              @click="onCopy"
            />
          </p>
        </template>

        <template v-else>Неверный ключ шифрования</template>
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

.text {
  position: relative;

  :global(.p-skeleton) {
    position: absolute !important;
    top: 50%;
    left: 0;
    width: calc(100% + 0.5rem) !important;
    height: 1.5rem !important;
    transform: translateY(-50%);
  }
}

.copy {
  cursor: pointer;
}
</style>
