<script setup>
import ToShow from '@/components/ToShow.vue'
// import TimeLine from '@/components/TimeLine.vue'
import postgres_api from '@/apis/postgres_api.js'
import { ref, onMounted } from 'vue'


const cirriculumVirtue = ref(null)

onMounted(() => {
  postgres_api.getWorkingExperiences()
    .then((response) => {
      cirriculumVirtue.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
})
</script>

<template>
  
  <h1> outer </h1>
    <v-row>
      <h2> row 1 </h2>
      <v-col>
        <h3>kol 1</h3>
      </v-col>
      <v-col>
        <h3>kol 2</h3>

        
      
      </v-col>
  
    </v-row>

    <v-row>
      <h2> row 2 </h2>
      <v-col>
        <h3>kol 1</h3>
      </v-col>
      <v-col>
        <h3>kol 2</h3>
      </v-col>

    </v-row>

  <div class="to-show">
      <!-- Setting a forloop to dispaly the events with a specific key -->
    <ToShow v-for = "work_experiences in cirriculumVirtue" :key = "work_experiences.id" :work_experiences = "work_experiences"   />
  </div>


</template>

<style scoped>
.to-show {
  display: flex;
  flex-direction: column;
  align-items: center;
}</style>
