import { createRouter, createWebHistory } from 'vue-router';
import AuthLayout from '@/layouts/AuthLayout.vue';
import MainLayout from '@/layouts/MainLayout.vue';
import AuthView from '@/views/AuthView.vue';
import NewSecretView from '@/views/NewSecretView.vue';
import TicketsView from '@/views/TicketsView.vue';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        { path: '/', name: 'tickets', component: TicketsView },
        { path: '/secrets/new', name: 'new-secret', component: NewSecretView },
      ],
    },
    {
      path: '/',
      component: AuthLayout,
      children: [{ path: '/auth', name: 'auth', component: AuthView }],
    },
  ],
});
