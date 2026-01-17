<script setup>
import { computed } from 'vue'
import masterData from '../../master_data.json'

// Import TimeLine and EducationLine components
import TimeLine from './cv/TimeLine.vue'
import EducationLine from './cv/EducationLine.vue'

// Get data from master_data.json
const docGen = masterData.document_generation_officer

// Get skills grouped by domain
const technicalSkills = computed(() =>
  docGen.skills.filter(s => s.domain === 'technical').map(s => s.name)
)

const softSkills = computed(() =>
  docGen.skills.filter(s => s.domain === 'soft_skills').slice(0, 10).map(s => s.name)
)

// Get certifications
const certifications = computed(() => docGen.certifications || [])

// Get hobbies
const hobbies = computed(() => docGen.hobbies || [])

// Personal info
const personalInfo = computed(() => docGen.personal_info)

// Currently learning skills (you can customize this list)
const learningSkills = ['RAG Pipelines', 'LangChain', 'LangGraph', 'Agent Architectures', 'FastAPI', 'Docker', 'Azure']

// Books (keeping static as not in JSON)
const books = [
  'AI Engineering — Chip Huyen',
  'Generative AI with LangChain — Auffarth & Kuligin',
  'Building Event-Driven Microservices',
  'Graph Data Science with Neo4j',
  'Designing Machine Learning Systems'
]
</script>

<template>
  <div>
    <!-- Hero Section -->
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6" variant="flat">
            <v-card-title class="text-h4 font-weight-bold">About</v-card-title>
            <v-card-text class="text-body-1">
              Career changer with an MSc in Data Science from SDU. Zero professional experience in the field—my background is hospitality and operations. Completed thesis work on NLP and transformers. Now actively learning while looking for my first data science or AI role.
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- The Story -->
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6">
            <v-card-title class="text-h5">The Story</v-card-title>
            <v-card-text class="text-body-1">
              <p class="mb-4">
                I spent a decade in hospitality and operations across Denmark, the Netherlands, Greece, and Australia. Bartending, hotels, back office, project management. Then I decided to change direction.
              </p>
              <p class="mb-4">
                I went back to school. First a Bachelor's in Economics & IT, then a Master's in Data Science. My thesis focused on NLP—transformer models for abstractive summarization and named entity recognition.
              </p>
              <p>
                Now I have the degree but not the experience. I'm at zero professionally in data science and AI. I'm honest about that. What I'm doing is learning aggressively on my own—RAG systems, LangChain, agent architectures, MLOps concepts—while looking for my first opportunity to work in the field.
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Education Section - using EducationLine component -->
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6">
            <v-card-title class="text-h5">
              <v-icon class="mr-2">mdi-school</v-icon>
              Education
            </v-card-title>
            <v-card-text>
              <EducationLine />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Technical Skills -->
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6">
            <v-card-title class="text-h5">
              <v-icon class="mr-2">mdi-code-tags</v-icon>
              Technical
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="4">
                  <p class="text-subtitle-2 font-weight-bold mb-2">Technical Skills:</p>
                  <div class="mb-4">
                    <v-chip v-for="skill in technicalSkills.slice(0, 15)" :key="skill" class="ma-1" size="small">
                      {{ skill }}
                    </v-chip>
                  </div>
                </v-col>
                <v-col cols="12" md="4">
                  <p class="text-subtitle-2 font-weight-bold mb-2">Currently learning:</p>
                  <div class="mb-4">
                    <v-chip v-for="skill in learningSkills" :key="skill" class="ma-1" size="small" color="secondary">
                      {{ skill }}
                    </v-chip>
                  </div>
                </v-col>
                <v-col cols="12" md="4">
                  <p class="text-subtitle-2 font-weight-bold mb-2">Certifications:</p>
                  <div>
                    <v-chip
                      v-for="cert in certifications"
                      :key="cert.name"
                      color="primary"
                      size="small"
                      class="ma-1"
                    >
                      <v-icon start size="small">mdi-certificate</v-icon>
                      {{ cert.name }}
                    </v-chip>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Work History Section - using TimeLine component -->
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6">
            <v-card-title class="text-h5">
              <v-icon class="mr-2">mdi-briefcase</v-icon>
              Work History
            </v-card-title>
            <v-card-text>
              <TimeLine />
              <v-alert type="info" variant="tonal" class="mt-4">
                None of this was data science. I have work experience, just not in the field I studied.
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Projects -->
      <v-row>
        

        <!-- Currently Reading -->
        <v-col cols="12" md="6">
          <v-card class="mb-6" height="100%">
            <v-card-title class="text-h5">
              <v-icon class="mr-2">mdi-book-open-page-variant</v-icon>
              Currently Reading
            </v-card-title>
            <v-card-text>
              <v-list density="compact">
                <v-list-item v-for="book in books" :key="book">
                  <template #prepend>
                    <v-icon size="small">mdi-book</v-icon>
                  </template>
                  <v-list-item-title>{{ book }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Outside Work -->
      <v-row>
        <v-col cols="12" md="6">
          <v-card class="mb-6">
            <v-card-title class="text-h5">
              <v-icon class="mr-2">mdi-heart</v-icon>
              Outside Work
            </v-card-title>
            <v-card-text>
              <div class="d-flex flex-wrap ga-2">
                <v-chip v-for="hobby in hobbies" :key="hobby" variant="outlined">
                  {{ hobby }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        
      </v-row>
    </v-container>
  </div>
</template>

<style scoped>
/* Profile page specific styles */
</style>
