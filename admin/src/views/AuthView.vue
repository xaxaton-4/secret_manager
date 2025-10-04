<script setup lang="ts">
import { reactive, ref } from 'vue';
import Form, { FormSubmitEvent } from '@primevue/forms/form';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { Button, Card, InputText, Message, useToast } from 'primevue';
import { z } from 'zod';

const toast = useToast();

const initialValues = reactive({
  email: '',
  password: '',
});

const resolver = ref(
  zodResolver(
    z.object({
      email: z.email({ message: 'Некорректный email' }).min(1, { message: 'Введите email' }),
      password: z.string().min(1, { message: 'Введите пароль' }),
    }),
  ),
);

const onFormSubmit = (event: FormSubmitEvent) => {
  if (event.valid) {
    toast.add({
      severity: 'success',
      summary: 'Form is submitted.',
      life: 3000,
    });
  }
};
</script>

<template>
  <Card :class="$style.card">
    <template #title>Авторизация</template>

    <template #content>
      <Form
        :class="$style.form"
        v-slot="$form"
        :initialValues="initialValues"
        :resolver="resolver"
        @submit="onFormSubmit"
        class="flex flex-col gap-4 w-full sm:w-56"
      >
        <div class="flex flex-col gap-1">
          <InputText
            name="email"
            type="text"
            placeholder="Email"
            fluid
          />
          <Message
            v-if="$form.email?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.email.error?.message }}
          </Message>
        </div>

        <div class="flex flex-col gap-1">
          <InputText
            name="password"
            type="password"
            placeholder="Пароль"
            fluid
          />
          <Message
            v-if="$form.password?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.password.error?.message }}
          </Message>
        </div>

        <Button
          type="submit"
          severity="secondary"
          label="Войти"
        />
      </Form>
    </template>
  </Card>
</template>

<style module lang="scss">
.card {
  width: 100%;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
