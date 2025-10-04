<script setup lang="ts">
import { computed, onMounted } from 'vue';
import dayjs from 'dayjs';
import { Card } from 'primevue';
import Chart from 'primevue/chart';
import { useTicketsStore } from '@/store/tickets';
import { capitalizeFirstLetter } from '@/utils/strings';

const ticketsStore = useTicketsStore();

const barChartData = computed(() => {
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

const pieChartData = computed(() => {
  const data = ticketsStore.tickets.reduce<Record<string, number>>(
    (acc, ticket) => {
      acc[ticket.is_approved ? 'Принятые' : 'Не принятые']++;
      return acc;
    },
    {
      Принятые: 0,
      'Не принятые': 0,
    },
  );

  return {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'Обработанные/не принятые заявки',
        data: Object.values(data),
      },
    ],
  };
});

const usersBarChartData = computed(() => {
  const data = ticketsStore.tickets.reduce<Record<string, number>>((acc, ticket) => {
    acc[ticket.user.email] = acc[ticket.user.email] ? acc[ticket.user.email] + 1 : 1;
    return acc;
  }, {});

  return {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'Заявки пользователей',
        data: Object.values(data),
      },
    ],
  };
});

const usersBarChartOptions = {
  indexAxis: 'y',
};

onMounted(() => {
  ticketsStore.getTickets();
});
</script>

<template>
  <div :class="$style.view">
    <Card>
      <template #title>Количество заявок по месяцам</template>

      <template #content>
        <Chart
          type="bar"
          :data="barChartData"
        />
      </template>
    </Card>

    <Card>
      <template #title>Принятые/не принятые заявки</template>

      <template #content>
        <Chart
          type="pie"
          :data="pieChartData"
        />
      </template>
    </Card>

    <Card>
      <template #title>Заявки пользователей</template>

      <template #content>
        <Chart
          type="bar"
          :data="usersBarChartData"
          :options="usersBarChartOptions"
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
</style>
