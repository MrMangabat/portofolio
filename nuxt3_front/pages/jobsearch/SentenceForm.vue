<!-- frontend/src/components/jobsearch_view/SentenceForm.vue -->

<script setup>
import GenericForm from '~/components/GenericForm.vue'
import jobsearch_api from '~/apis/jobsearch_api'
import { useRemoveSentencesList } from '@/stores/removeSentencesList'

const store = useRemoveSentencesList()
</script>

<template>
  <GenericForm
    :apiAddFn="jobsearch_api.addSentence"
    :piniaAddFn="store.piniaAddSentence.bind(store)"
    inputProperty="text"
    label="Add invalid sentences/phrases"
    validationErrorMessage="Invalid input: sentence is either empty or not a string."
  />
</template>

<style scoped>
.centered-label ::v-deep .v-field-label {
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
