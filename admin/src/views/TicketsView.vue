<script setup lang="ts">
import { computed, onMounted } from 'vue';
import dayjs from 'dayjs';
import { ProgressSpinner } from 'primevue';
import Button from 'primevue/button';
import Card from 'primevue/card';
import { useConfirm } from 'primevue/useconfirm';
import { useTicketsStore } from '@/store/tickets';

const ticketsStore = useTicketsStore();
const confirm = useConfirm();

const tickets = computed(() => {
  return ticketsStore.tickets.filter((ticket) => !ticket.is_approved);
});

const onAccept = (event: PointerEvent, ticketId: number) => {
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
      ticketsStore.approveTicket(ticketId);
    },
  });
};

const onReject = (event: PointerEvent, ticketId: number) => {
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
      ticketsStore.deleteTicket(ticketId);
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

    <ProgressSpinner v-if="ticketsStore.isLoading" />

    <template v-else>
      <Card
        v-for="ticket in tickets"
        :key="ticket.id"
      >
        <template #title>Заявка от {{ ticket.user.email }}</template>
        <template #content>
          <p>Ресурс: {{ ticket.resource }}</p>
          <p>Обоснование: {{ ticket.reason }}</p>
          <p>Срок доступа: {{ dayjs(ticket.period).format('DD.MM.YYYY') }}</p>
        </template>

        <template #footer>
          <Button
            label="Принять"
            icon="pi pi-check"
            :class="$style.accept"
            @click="onAccept($event, ticket.id)"
          />
          <Button
            label="Отклонить"
            icon="pi pi-times"
            severity="danger"
            @click="onReject($event, ticket.id)"
          />
        </template>
      </Card>
    </template>
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
