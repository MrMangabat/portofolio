<!-- frontend/src/components/jobsearch_view/WordsForm.vue -->

<script setup>
import { useItemForm } from '@/composables/useItemForm';
import jobsearch_api from '../../apis/jobsearch_api';
import { useRemoveWordsList } from '@/stores/removeWordsList';

const store = useRemoveWordsList();

const { item, addItemAndClear } = useItemForm({
  apiAddFunction: jobsearch_api.addWord,
  piniaAddFunction: store.piniaAddWord.bind(store),
  inputProperty: 'text',
  validationErrorMessage: 'Invalid input: word is either empty or not a string.',
});
</script>

<template>
  <div>
    <form @submit.prevent="addItemAndClear">
      <!-- Input Field Row with Top Margin -->
      <v-row class="mt-3">
        <v-col cols="12">
          <v-text-field
            v-model="item.text"
            label="Add invalid words"
            type="text"
            style="width: 100%; margin-bottom: -30px;"
            class="centered-label"
          />
        </v-col>
      </v-row>
      <!-- Add Button Row with Bottom Margin -->
      <v-row class="mb-3">
        <v-col cols="12" class="d-flex justify-center">
          <v-btn type="submit" color="primary">
            Add
          </v-btn>
        </v-col>
      </v-row>
    </form>
  </div>
</template>

<style scoped>
.centered-label :v-deep .v-field-label {
  text-align: center;
  width: 100%;
}

.mt-3 {
  margin-top: 12px; /* Adjusted from 16px to 12px */
}

.mb-3 {
  margin-bottom: 12px; /* Adjusted from 16px to 12px */
}
</style>
