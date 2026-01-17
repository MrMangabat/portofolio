<script setup>
import { computed } from 'vue'
import masterData from '../../../master_data.json'

// Get education data from master_data.json
const rawEducation = masterData.document_generation_officer.education

// Transform data to match template expectations
const educations = computed(() => {
  return rawEducation.map((edu, index) => ({
    id: index,
    school_name: edu.institution,
    degree: edu.degree,
    location: edu.location,
    start_date: edu.start_date,
    end_date: edu.end_date,
    current: edu.current,
    gpa: edu.gpa_danish || edu.gpa_international || '',
    description: edu.condensed_description_bulletpoints?.filter(d => d).join(' | ') || ''
  }))
})

// Split into two columns
const leftColumn = computed(() => educations.value.slice(0, Math.ceil(educations.value.length / 2)))
const rightColumn = computed(() => educations.value.slice(Math.ceil(educations.value.length / 2)))
</script>

<template>
  <v-container>
    <div>
      <v-row>
        <v-col cols="12" md="6">
          <div v-for="education in leftColumn" :key="education.id">
            <v-card class="edu-line" density="compact" variant="outlined">
              <v-card-title class="text-subtitle-1">
                {{ education.school_name }}
              </v-card-title>
              <v-card-subtitle>
                {{ education.degree }}
              </v-card-subtitle>
              <v-card-text>
                <span class="text-caption text-grey">{{ education.location }}</span>
                <br>
                <v-chip size="x-small" color="primary" variant="outlined" class="mt-1">
                  {{ education.start_date }} - {{ education.end_date }}
                </v-chip>
                <span v-if="education.gpa" class="ml-2 text-caption">
                  GPA: {{ education.gpa }}
                </span>
                <p v-if="education.description" class="mt-2 text-body-2">
                  {{ education.description }}
                </p>
              </v-card-text>
            </v-card>
          </div>
        </v-col>
        <v-col cols="12" md="6">
          <div v-for="education in rightColumn" :key="education.id">
            <v-card class="edu-line" density="compact" variant="outlined">
              <v-card-title class="text-subtitle-1">
                {{ education.school_name }}
              </v-card-title>
              <v-card-subtitle>
                {{ education.degree }}
              </v-card-subtitle>
              <v-card-text>
                <span class="text-caption text-grey">{{ education.location }}</span>
                <br>
                <v-chip size="x-small" color="primary" variant="outlined" class="mt-1">
                  {{ education.start_date }} - {{ education.end_date }}
                </v-chip>
                <span v-if="education.gpa" class="ml-2 text-caption">
                  GPA: {{ education.gpa }}
                </span>
                <p v-if="education.description" class="mt-2 text-body-2">
                  {{ education.description }}
                </p>
              </v-card-text>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>



<style scoped>
    .edu-line {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px;
      /* height: 200px; */
      /* width: 400px; */
      /* border: 1px solid #39495c; */
      margin-bottom: 30px;
    }
    .edu-logo {
      margin-top: 20px
    }
    .row1 {
      
      justify-content: center;
      
      margin-top: -30px;
      margin-bottom: -60px;
    }
    .row2 {
    
      justify-content: center;
      align-items: center;
      margin-top: -30px;
      margin-bottom: -60px;
    }

</style>