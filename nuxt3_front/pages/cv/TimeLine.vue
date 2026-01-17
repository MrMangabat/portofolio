<script setup>
import { ref, computed } from 'vue'
import masterData from '../../../master_data.json'

// Get work experiences from master_data.json
const rawWorkExperiences = masterData.document_generation_officer.work_experience

// Transform data to match template expectations
const workExperiences = computed(() => {
  return rawWorkExperiences.map((exp, index) => ({
    id: index,
    job_title: exp.position,
    company_name: exp.company,
    location: exp.location,
    start_date: exp.start_date,
    end_date: exp.end_date,
    current: exp.current,
    // Join detailed description or use condensed bullet points
    job_description: exp.detailed_description?.filter(d => d).join(' ') ||
                     exp.condensed_description_bulletpoints?.join(' | ') || '',
    bullet_points: exp.condensed_description_bulletpoints || []
  }))
})
</script>

<template>
  <v-container>
    <div
      class="work-timeline"
      style="max-height: 800px; overflow-y: auto;">

      <v-timeline side="end">
        <v-timeline-item
          v-for="work_experience in workExperiences"
          :key="work_experience.id"
          :dot-color="work_experience.current ? 'success' : 'primary'"
        >
          <template v-slot:default>
            <v-card class="elevation-2">
              <v-card-title class="text-subtitle-1">
                {{ work_experience.job_title }}
              </v-card-title>
              <v-card-text>
                <ul v-if="work_experience.bullet_points.length > 0" class="bullet-list">
                  <li v-for="(point, idx) in work_experience.bullet_points" :key="idx">
                    {{ point }}
                  </li>
                </ul>
                <p v-else>{{ work_experience.job_description }}</p>
              </v-card-text>
            </v-card>
          </template>
          <template v-slot:opposite>
            <div class="text-right">
              <span class="company-name font-weight-bold">
                {{ work_experience.company_name }}
              </span>
              <br>
              <span class="text-caption text-grey">
                {{ work_experience.location }}
              </span>
              <br>
              <v-chip
                size="x-small"
                :color="work_experience.current ? 'success' : 'default'"
                variant="outlined"
                class="mt-1"
              >
                {{ work_experience.start_date }} - {{ work_experience.end_date }}
              </v-chip>
            </div>
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