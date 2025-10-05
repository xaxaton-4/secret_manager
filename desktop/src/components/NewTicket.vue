<script setup lang="ts">
import { ref, reactive } from 'vue';
import { Form, FormSubmitEvent } from '@primevue/forms';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { InputText, Message, Button, Card, DatePicker } from 'primevue';
import { z } from 'zod';

interface FormValues {
  resource: string;
  reason: string;
  period: Date | null;
}

const props = defineProps<{
  initialResource?: string;
  isLoading?: boolean;
}>();

const emit = defineEmits<{
  (e: 'submit', values: FormValues): void;
  (e: 'back'): void;
}>();

const initialValues = reactive<FormValues>({
  resource: props.initialResource || '',
  reason: '',
  period: null,
});

const resolver = ref(
  zodResolver(
    z.object({
      resource: z.string().min(1, { message: 'Введите ресурс' }),
      reason: z.string().min(1, { message: 'Введите обоснование' }),
      period: z.preprocess(
        (value: string) => {
          if (!value) return null;
          return new Date(value);
        },
        z.union([
          z.date(),
          z.null().refine((value) => value !== null, { message: 'Введите срок доступа' }),
        ]),
      ),
    }),
  ),
);

const onFormSubmit = (event: FormSubmitEvent) => {
  if (event.valid) {
    emit('submit', event.values as FormValues);
  }
};
</script>

<template>
  <Card :class="$style.card">
    <template #title>
      <Button
        icon="pi pi-arrow-left"
        severity="secondary"
        aria-label="Назад"
        @click="$emit('back')"
      />

      Заявка на доступ
    </template>

    <template #content>
      <Form
        v-slot="$form"
        :initialValues="initialValues"
        :resolver="resolver"
        @submit="onFormSubmit"
        :class="$style.form"
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
            name="reason"
            type="text"
            placeholder="Обоснование"
            fluid
          />
          <Message
            v-if="$form.reason?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.reason.error?.message }}
          </Message>
        </div>

        <div class="flex flex-col gap-1">
          <DatePicker
            name="period"
            placeholder="Срок доступа"
            dateFormat="dd.mm.yy"
            updateModelType="date"
            :minDate="new Date()"
            fluid
          />
          <Message
            v-if="$form.period?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.period.error?.message }}
          </Message>
        </div>

        <Button
          type="submit"
          label="Создать"
          :loading="isLoading"
        />
      </Form>
    </template>
  </Card>
</template>

<style module lang="scss">
.card {
  position: relative;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
