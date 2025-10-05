import { createApp } from 'vue';
import Aura from '@primeuix/themes/aura';
import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import Tooltip from 'primevue/tooltip';
import App from './App.vue';
import './assets/style.scss';
import { store } from './core/store';

const app = createApp(App);

app.use(store);

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: false,
    },
  },
  locale: {
    dayNamesMin: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
    monthNames: [
      'Январь',
      'Февраль',
      'Март',
      'Апрель',
      'Май',
      'Июнь',
      'Июль',
      'Август',
      'Сентябрь',
      'Октябрь',
      'Ноябрь',
      'Декабрь',
    ],
    firstDayOfWeek: 1,
  },
});

app.use(ToastService);
app.use(ConfirmationService);

app.directive('tooltip', Tooltip);

app.mount('#app');

export const toast = app.config.globalProperties.$toast;
