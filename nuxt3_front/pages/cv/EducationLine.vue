<script setup>

import postgres_api from '@/apis/jobsearch_api.js'
import { ref, onMounted } from 'vue'


const edu_achievements = ref([])

onMounted(() => {
  postgres_api.getEducation()
    .then((response) => {
        edu_achievements.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
})

defineProps({
  educations: {
    type: Object,
    required: true
  },
})

</script>

<template>
  <v-container>
    <div>
      <v-row>
        <v-col>
          <div v-for="(education, index) in edu_achievements.slice(0, Math.ceil(edu_achievements.length / 2))" :key="education.edu_id" :education="education">
            <v-card class="edu-line" density="compact">
              <v-row class="row1">
                <v-col>
                  <v-card-title>
                    {{ education.school_name }}
                  </v-card-title>
                  <v-card-text>
                    {{ education.degree }}
                    <br>
                    {{ education.start_date }} - {{ education.end_date }}
                  </v-card-text>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-avatar class="edu-logo" size="80" rounded="1">
                    <v-img :src="education.image_path"></v-img>
                  </v-avatar>
                </v-col>
              </v-row>
            </v-card>
          </div>
        </v-col>
        <v-col>
          <div v-for="(education, index) in edu_achievements.slice(Math.ceil(edu_achievements.length / 2))" :key="education.edu_id" :education="education">
            <v-card class="edu-line" density="compact">
              <v-row class="row2">
                <v-col>
                  <v-card-title>
                    {{ education.school_name }}
                  </v-card-title>
                  <v-card-text>
                    {{ education.degree }}
                    <br>
                    {{ education.start_date }} - {{ education.end_date }}
                  </v-card-text>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-avatar class="edu-logo" size="80" rounded="1">
                    <v-img :src="education.image_path"></v-img>
                  </v-avatar>
                </v-col>
              </v-row>
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