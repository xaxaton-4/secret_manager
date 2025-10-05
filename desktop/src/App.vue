<script setup lang="ts">
import { ref, onMounted } from 'vue';
import dayjs from 'dayjs';
import { Card, Toast, useConfirm, useToast } from 'primevue';
import ConfirmDialog from 'primevue/confirmdialog';
import { createTicket } from './api/tickets';
import Auth from './components/Auth.vue';
import Container from './components/Container.vue';
import NewTicket from './components/NewTicket.vue';
import Search from './components/Search.vue';
import Secret from './components/Secret.vue';
import { useAuthStore } from './store/auth';
import { useSecretsStore } from './store/secrets';

const authStore = useAuthStore();
const secretsStore = useSecretsStore();
const toast = useToast();
const confirm = useConfirm();

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

const onSearch = (resource: string) => {
  secretsStore.currentSecret = null;

  const secret = secretsStore.secrets[resource];
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

  secretsStore.currentSecret = {
    resource,
    value: secret,
  };

  toast.add({
    severity: 'success',
    summary: 'Секрет успешно найден',
    life: 3000,
  });
};

onMounted(() => {
  authStore.auth();
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

      <Search
        v-else
        @search="onSearch"
      />

      <Secret
        v-if="secretsStore.currentSecret"
        v-bind="secretsStore.currentSecret"
      />
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
