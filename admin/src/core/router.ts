import { createRouter, createWebHistory } from 'vue-router';
import AuthLayout from '@/layouts/AuthLayout.vue';
import MainLayout from '@/layouts/MainLayout.vue';
import { useAuthStore } from '@/store/auth';
import AuthView from '@/views/AuthView.vue';
import DashboardView from '@/views/DashboardView.vue';
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
        { path: '/dashboard', name: 'dashboard', component: DashboardView },
      ],
    },
    {
      path: '/',
      component: AuthLayout,
      meta: { isPublic: true },
      children: [{ path: '/auth', name: 'auth', component: AuthView }],
    },
  ],
});

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore();

  if (to.name !== 'auth' && !authStore.isAuth) {
    await authStore.auth();
    if (authStore.isAuth) {
      return next();
    }
  } else {
    authStore.isReady = true;
  }

  if (!to.meta.isPublic && !authStore.isAuth) {
    return next('/auth');
  }

  next();
});
