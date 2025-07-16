<!-- frontend/src/components/jobsearch_view/SkillsetForm.vue -->

<script setup>
import GenericForm from '~/components/GenericForm.vue'
import jobsearch_api from '~/apis/jobsearch_api'
import { useSkillset } from '@/stores/skillSetStore'

const store = useSkillset()
</script>

<template>
  <GenericForm
    :apiAddFn="jobsearch_api.addSkill"
    :piniaAddFn="store.piniaAddSkill.bind(store)"
    inputProperty="skill"
    label="Add your skill"
    validationErrorMessage="Invalid input: skill is either empty or not a string."
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
