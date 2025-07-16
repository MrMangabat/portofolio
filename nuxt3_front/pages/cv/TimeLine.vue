<script setup>
import postgres_api from '@/apis/jobsearch_api.js'
import { ref, onMounted } from 'vue'

//getting the data from the postgres_api.js for working expericences
const cirriculumVirtue = ref(null)

//getting the local images files from the assets folder

onMounted(() => {
  postgres_api.getWorkingExperiences()
    .then((response) => {
      cirriculumVirtue.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
})

defineProps({
  work_experiences: {
    type: Object,
    required: true
  },
})


</script>
<template>
  <v-container>
    <div 
      class="work timeline"
      style="height: 800px; 
      overflow-y: auto;">

      <v-timeline side="end">
        <v-timeline-item v-for="work_experience in cirriculumVirtue" :key="work_experience.id">
          <template v-slot:icon>
            <v-avatar>
              <v-img
                :width="300"
                aspect-ratio="16/9"
                :src="work_experience.image_path"
              ></v-img>
            </v-avatar>
          </template>
          <template v-slot:default>
            <v-card class="elevation-2">
              <v-card-title>
                <span class="job-title">
                  {{ work_experience.job_title }}
                </span>
              </v-card-title>
              <v-card-text>
                  {{ work_experience.job_description }}
              </v-card-text>
              <v-card-text></v-card-text>
            </v-card>
          </template>
          <template v-slot:opposite>
            <span class="company-name">
              {{ work_experience.company_name }}
            </span>
            <br>
            <span class="company-end-dates">
              End date: {{ work_experience.end_date }}
            </span>
            <br>
            <span class="company-start-dates">
              Start date: {{ work_experience.start_date }}
            </span>
          </template>
        </v-timeline-item>
      </v-timeline>
    </div>

    

  </v-container>
</template>

<style scoped>
.company-name {
        font-weight: bold;
      }
</style>