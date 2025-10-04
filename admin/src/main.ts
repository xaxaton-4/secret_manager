import { createApp } from 'vue';
import Aura from '@primeuix/themes/aura';
import dayjs from 'dayjs';
import 'dayjs/locale/ru';
import { createPinia } from 'pinia';
import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import Tooltip from 'primevue/tooltip';
import App from './App.vue';
import './assets/style.scss';
import { router } from './core/router';

dayjs.locale('ru');

const app = createApp(App);

app.use(ToastService);
app.use(ConfirmationService);

app.use(router);

app.use(createPinia());

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: false,
    },
  },
});

app.directive('tooltip', Tooltip);

app.mount('#app');

export const toast = app.config.globalProperties.$toast;
