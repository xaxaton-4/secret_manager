<script setup lang="ts">
import { ref } from 'vue';
import { reactive } from 'vue';
import { Form, FormSubmitEvent } from '@primevue/forms';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { Button, Dialog, InputText, Message } from 'primevue';
import z from 'zod';

interface FormValues {
  key: string;
}

defineProps<{
  isVisible: boolean;
  isLoading?: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:is-visible', isVisible: boolean): void;
  (e: 'close'): void;
  (e: 'submit', key: string): void;
}>();

const initialValues = reactive<FormValues>({
  key: '',
});

const resolver = ref(
  zodResolver(
    z.object({
      key: z.string().min(1, { message: 'Введите ключ' }),
    }),
  ),
);

const onFormSubmit = (event: FormSubmitEvent) => {
  if (event.valid) {
    emit('submit', (event.values as FormValues).key);
  }
};
</script>

<template>
  <Dialog
    :visible="isVisible"
    modal
    :class="$style.dialog"
    header="Ключ шифрования"
    @update:visible="$emit('update:is-visible', $event)"
  >
    <Form
      v-slot="$form"
      :class="$style.form"
      :initialValues="initialValues"
      :resolver="resolver"
      @submit="onFormSubmit"
      class="flex flex-col gap-4 w-full sm:w-56"
    >
      <div class="flex flex-col gap-1">
        <InputText
          name="key"
          type="text"
          placeholder="Ключ"
          fluid
        />
        <Message
          v-if="$form.key?.invalid"
          severity="error"
          size="small"
          variant="simple"
        >
          {{ $form.key.error?.message }}
        </Message>
      </div>

      <div>
        <Button
          type="button"
          label="Отменить"
          severity="secondary"
          :class="$style.cancel"
          @click="$emit('close')"
        />
        <Button
          type="submit"
          label="Сохранить"
        />
      </div>
    </Form>
  </Dialog>
</template>

<style module lang="scss">
.dialog {
  width: 25rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cancel {
  margin-right: 0.5rem;
}
</style>
