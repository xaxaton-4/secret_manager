<script setup lang="ts">
import { reactive, ref } from 'vue';
import Form, { FormSubmitEvent } from '@primevue/forms/form';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { Button, Card, InputText, Message } from 'primevue';
import { z } from 'zod';
import { useSecretsStore } from '@/store/secrets';
import { encryptAES } from '@/utils/crypt';

interface FormValues {
  resource: string;
  value: string;
  encryptionKey: string;
}

const secretsStore = useSecretsStore();

const initialValues = reactive<FormValues>({
  resource: '',
  value: '',
  encryptionKey: '',
});

const resolver = ref(
  zodResolver(
    z.object({
      resource: z.string().min(1, { message: 'Введите ресурс' }),
      value: z.string().min(1, { message: 'Введите значение' }),
      encryptionKey: z.string().min(1, { message: 'Введите ключ шифрования' }),
    }),
  ),
);

const onFormSubmit = async (event: FormSubmitEvent) => {
  if (event.valid) {
    const values = event.values as FormValues;
    secretsStore.createSecret({
      resource: values.resource,
      value: await encryptAES(values.value, values.encryptionKey),
    });
  }
};
</script>

<template>
  <Card>
    <template #title>Новый секрет</template>

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
            name="resource"
            type="text"
            placeholder="Ресурс"
            fluid
          />
          <Message
            v-if="$form.resource?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.resource.error?.message }}
          </Message>
        </div>

        <div class="flex flex-col gap-1">
          <InputText
            name="value"
            type="text"
            placeholder="Значение"
            fluid
          />
          <Message
            v-if="$form.value?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.value.error?.message }}
          </Message>
        </div>

        <div class="flex flex-col gap-1">
          <InputText
            name="encryptionKey"
            type="text"
            placeholder="Ключ шифрования"
            fluid
          />
          <Message
            v-if="$form.encryptionKey?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.encryptionKey.error?.message }}
          </Message>
        </div>

        <Button
          type="submit"
          severity="secondary"
          label="Создать"
        />
      </Form>
    </template>
  </Card>
</template>

<style module lang="scss">
.form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
