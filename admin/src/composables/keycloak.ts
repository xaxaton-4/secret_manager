import { computed, ref, watch } from 'vue';
import Keycloak from 'keycloak-js';

// import { useAuthStore } from '@/store/auth';

const keycloak = new Keycloak({
  url: 'http://localhost:8081',
  realm: 'master',
  clientId: 'client-id',
});

const isAuthenticated = ref(false);

keycloak.onAuthSuccess = async () => {
  console.log(keycloak.tokenParsed);
  isAuthenticated.value = true;
};

export const useKeycloak = () => {
  const user = computed(() => keycloak.tokenParsed);

  watch(
    user,
    (user) => {
      console.log(user);
    },
    { immediate: true },
  );

  return {
    keycloak,
    isAuthenticated,
    user,
  };
};
