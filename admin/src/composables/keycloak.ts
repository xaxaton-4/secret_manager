import { computed, ref, watch } from 'vue';
import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL,
  realm: import.meta.env.VITE_KEYCLOAK_REALM,
  clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID,
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
