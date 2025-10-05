<script setup lang="ts">
import { ref, reactive } from 'vue';
import { Form, FormSubmitEvent } from '@primevue/forms';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { InputText, Message, Button, Card } from 'primevue';
import { z } from 'zod';

const emit = defineEmits<{
  (e: 'search', resource: string): void;
}>();

const initialValues = reactive({
  resource: '',
});

const resolver = ref(
  zodResolver(
    z.object({
      resource: z
        .string()
        .min(1, { message: 'Введите ресурс' })
        .refine((value) => !value.includes(' '), {
          message: 'Ресурс не должен содержать пробелы',
        }),
    }),
  ),
);

const onFormSubmit = (event: FormSubmitEvent) => {
  if (event.valid) {
    emit('search', (event.values as { resource: string }).resource);
  }
};
</script>

<template>
  <Card>
    <template #title>Поиск</template>

    <template #content>
      <Form
        v-slot="$form"
        :initialValues="initialValues"
        :resolver="resolver"
        @submit="onFormSubmit"
        :class="$style.form"
        class="flex flex-col gap-4 w-full sm:w-56"
      >
        <div
          :class="$style.input"
          class="flex flex-col gap-1"
        >
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
        <Button
          v-tooltip.top="'Найти'"
          type="submit"
          icon="pi pi-search"
          aria-label="Найти"
        />
      </Form>
    </template>
  </Card>
</template>

<style module lang="scss">
.form {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.input {
  flex-grow: 1;
}
</style>
