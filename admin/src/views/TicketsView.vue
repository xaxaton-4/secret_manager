<script setup lang="ts">
import { onMounted } from 'vue';
import Button from 'primevue/button';
import Card from 'primevue/card';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';
import { useTicketsStore } from '@/store/tickets';

const ticketsStore = useTicketsStore();
const confirm = useConfirm();
const toast = useToast();

const onAccept = (event: PointerEvent) => {
  confirm.require({
    target: event.currentTarget as HTMLElement,
    message: 'Вы действительно хотите принять заявку?',
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
      toast.add({
        severity: 'info',
        summary: 'Confirmed',
        detail: 'You have accepted',
        life: 3000,
      });
    },
    reject: () => {
      toast.add({
        severity: 'error',
        summary: 'Rejected',
        detail: 'You have rejected',
        life: 3000,
      });
    },
  });
};

const onReject = (event: PointerEvent) => {
  confirm.require({
    target: event.currentTarget as HTMLElement,
    message: 'Вы действительно хотите отклонить заявку?',
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
      toast.add({
        severity: 'info',
        summary: 'Confirmed',
        detail: 'You have accepted',
        life: 3000,
      });
    },
    reject: () => {
      toast.add({
        severity: 'error',
        summary: 'Rejected',
        detail: 'You have rejected',
        life: 3000,
      });
    },
  });
};

onMounted(() => {
  ticketsStore.getTickets();
});
</script>

<template>
  <div :class="$style.view">
    <Card class="no-content-card">
      <template #title>Заявки</template>
    </Card>

    <Card>
      <template #title>Заявка от ...</template>
      <template #content>
        <p>Ресурс: ...</p>
        <p>Обоснование: ...</p>
        <p>Срок доступа: ...</p>
      </template>

      <template #footer>
        <Button
          label="Принять"
          icon="pi pi-check"
          :class="$style.accept"
          @click="onAccept($event)"
        />
        <Button
          label="Отклонить"
          icon="pi pi-times"
          severity="danger"
          @click="onReject"
        />
      </template>
    </Card>
  </div>
</template>

<style module lang="scss">
.view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.accept {
  margin-right: 1rem;
}
</style>
