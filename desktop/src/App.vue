<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { watch } from 'vue';
import dayjs from 'dayjs';
import { Card, ProgressSpinner, Toast, useConfirm, useToast } from 'primevue';
import ConfirmDialog from 'primevue/confirmdialog';
import { createTicket } from './api/tickets';
import Auth from './components/Auth.vue';
import Container from './components/Container.vue';
import EncryptionKeyForm from './components/EncryptionKeyForm.vue';
import NewTicket from './components/NewTicket.vue';
import NotLoadedSecret from './components/NotLoadedSecret.vue';
import Search from './components/Search.vue';
import Secret from './components/Secret.vue';
import { useSocket } from './composables/socket';
import { useAuthStore } from './store/auth';
import { useSecretsStore } from './store/secrets';

const authStore = useAuthStore();
const secretsStore = useSecretsStore();
const toast = useToast();
const confirm = useConfirm();
const { initSocket } = useSocket();

const encryptionKey = ref('');
const lastResource = ref('');
const isTicketLoading = ref(false);
const isNewTicketVisible = ref(false);

const onNewTicketBack = () => {
  isNewTicketVisible.value = false;
  lastResource.value = '';
};

const onCreateTicket = async (values: {
  resource: string;
  reason: string;
  period: Date | null;
}) => {
  isTicketLoading.value = true;
  try {
    await createTicket({
      resource: values.resource,
      reason: values.reason,
      period: dayjs(values.period).format('YYYY-MM-DD'),
    });
    toast.add({
      severity: 'success',
      summary: 'Заявка успешно создана',
      life: 3000,
    });
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось создать заявку',
      life: 3000,
    });
  } finally {
    isTicketLoading.value = false;
    onNewTicketBack();
  }
};

const onSearch = async (resource: string) => {
  const secret = secretsStore.secretsList.includes(resource);
  if (!secret) {
    confirm.require({
      message: 'Хотите создать заявку на доступ?',
      header: 'Не удалось найти секрет',
      icon: 'pi pi-exclamation-triangle',
      rejectProps: {
        label: 'Нет',
        severity: 'secondary',
        outlined: true,
      },
      acceptProps: {
        label: 'Да',
      },
      accept: () => {
        isNewTicketVisible.value = true;
        lastResource.value = resource;
      },
    });
    return;
  }

  await secretsStore.getSecret(resource);
};

const onEnterKey = (key: string) => {
  encryptionKey.value = key;
};

onMounted(() => {
  authStore.auth();
});

watch([() => authStore.isAuth, () => authStore.isReady], (isAuth, isReady) => {
  if (isAuth && isReady) {
    initSocket();
    secretsStore.getSecrets();
  }
});
</script>

<template>
  <Container v-if="authStore.isReady">
    <template v-if="authStore.isAuth">
      <Card class="no-content-card">
        <template #title>
          <div :class="$style.title">
            Секреты

            <i
              :class="$style.logout"
              class="pi pi-sign-out"
              v-tooltip="'Выйти'"
              @click="authStore.logout"
            />
          </div>
        </template>
      </Card>

      <NewTicket
        v-if="isNewTicketVisible"
        :initial-resource="lastResource"
        :is-loading="isTicketLoading"
        @submit="onCreateTicket"
        @back="onNewTicketBack"
      />

      <template v-else>
        <Search @search="onSearch" />

        <EncryptionKeyForm @submit="onEnterKey" />
      </template>

      <ProgressSpinner v-if="secretsStore.isLoading" />

      <template
        v-else
        v-for="resource in secretsStore.secretsList"
        :key="resource"
      >
        <Secret
          v-if="secretsStore.secretsVisible[resource]"
          :resource="resource"
          :value="secretsStore.secrets[resource]"
          :encryption-key="encryptionKey"
        />

        <NotLoadedSecret
          v-else
          :resource="resource"
        />
      </template>

      <!-- <Secret
        v-if="secretsStore.currentSecret && encryptionKey"
        :resource="secretsStore.currentSecret.resource"
        :value="secretsStore.currentSecret.value"
        :encryption-key="encryptionKey"
      /> -->
    </template>

    <Auth v-else />
  </Container>

  <Toast />
  <ConfirmDialog />
</template>

<style module lang="scss">
.title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logout {
  cursor: pointer;
}
</style>
