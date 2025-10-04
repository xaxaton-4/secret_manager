import { defineStore } from 'pinia';
import { getTickets } from '@/api/tickets';
import { toast } from '@/main';
import { TicketsState } from '@/types/tickets';
import { Role } from '@/types/users';

export const useTicketsStore = defineStore('tickets', {
  state: (): TicketsState => ({
    tickets: [],
    isLoading: false,
  }),
  actions: {
    async getTickets() {
      this.isLoading = true;
      try {
        // this.tickets = await getTickets();
        this.tickets = [
          {
            id: 1,
            resource: 'DB_MAIN_SERVER',
            reason: 'Резервное копирование базы данных',
            period: '2024-01-15',
            is_approved: true,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
          {
            id: 2,
            resource: 'API_AUTH_SERVICE',
            reason: 'Тестирование новой функциональности',
            period: '2024-01-18',
            is_approved: false,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
          {
            id: 3,
            resource: 'CACHE_REDIS_CLUSTER',
            reason: 'Обновление версии Redis',
            period: '2024-01-20',
            is_approved: true,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
          {
            id: 4,
            resource: 'STORAGE_S3_BUCKET',
            reason: 'Миграция данных в новый регион',
            period: '2024-01-22',
            is_approved: false,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
          {
            id: 5,
            resource: 'QUEUE_RABBITMQ',
            reason: 'Настройка мониторинга очередей',
            period: '2024-01-25',
            is_approved: true,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
          {
            id: 6,
            resource: 'LOG_ELASTICSEARCH',
            reason: 'Архивирование старых логов',
            period: '2024-01-28',
            is_approved: true,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
          {
            id: 7,
            resource: 'CDN_EDGE_NODES',
            reason: 'Развертывание нового контента',
            period: '2024-02-01',
            is_approved: false,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
          {
            id: 8,
            resource: 'DB_ANALYTICS_REPLICA',
            reason: 'Выполнение аналитических запросов',
            period: '2024-02-05',
            is_approved: true,
            user: {
              id: 1,
              email: 'example@org.ru',
              role: Role.User,
            },
          },
        ];
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Ошибка',
          detail: 'Не удалось загрузить заявки',
          life: 3000,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
});
