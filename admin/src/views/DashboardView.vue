<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import dayjs from 'dayjs';
import { Card } from 'primevue';
import Chart from 'primevue/chart';
import { useTicketsStore } from '@/store/tickets';
import { capitalizeFirstLetter } from '@/utils/strings';

const ticketsStore = useTicketsStore();

const chartData = computed(() => {
  const data = ticketsStore.tickets.reduce<Record<string, number>>((acc, ticket) => {
    const key = capitalizeFirstLetter(dayjs(ticket.period).format('MMMM YYYY'));
    acc[key] = acc[key] ? acc[key] + 1 : 1;
    return acc;
  }, {});

  return {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'Количество заявок по месяцам',
        data: Object.values(data),
      },
    ],
  };
});

onMounted(() => {
  ticketsStore.getTickets();
});
</script>

<template>
  <Card>
    <template #title>Количество заявок по месяцам</template>

    <template #content>
      <Chart
        type="bar"
        :data="chartData"
      />
    </template>
  </Card>
</template>

<style module lang="scss"></style>
