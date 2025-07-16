<!-- frontend/src/components/jobsearch_view/WordsForm.vue -->

<script setup>
import GenericForm from '~/components/GenericForm.vue'
import jobsearch_api from '~/apis/jobsearch_api'
import { useRemoveWordsList } from '@/stores/removeWordsList'

const store = useRemoveWordsList()
</script>

<template>
  <GenericForm
    :apiAddFn="jobsearch_api.addWord"
    :piniaAddFn="store.piniaAddWord.bind(store)"
    inputProperty="text"
    label="Add invalid words"
    validationErrorMessage="Invalid input: word is either empty or not a string."
  />
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
