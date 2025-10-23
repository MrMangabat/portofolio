<script setup>
import { ref } from 'vue'
import { useItemForm } from '~/composables/useItemForm'
import { useItemList } from '~/composables/useItemList'
import { useJobSearchApi } from '~/composables/useJobSearchApi'
import { useSkillset } from '~/stores/skillSetStore'
import { useRemoveWordsList } from '~/stores/removeWordsList'
import { useRemoveSentencesList } from '~/stores/removeSentencesList'
import FileUploads from './FileUploads.vue'

// Initialize API and stores
const api = useJobSearchApi()
const skillStore = useSkillset()
const wordsStore = useRemoveWordsList()
const sentencesStore = useRemoveSentencesList()

// Cover letter generation state
const jobDescription = ref('')
const userInput = ref('')
const generatedCoverLetter = ref(null)
const isGenerating = ref(false)
const generationError = ref(null)

// Generate cover letter function
const generateCoverLetter = async () => {
  if (!jobDescription.value.trim()) {
    generationError.value = 'Please enter a job description'
    return
  }

  isGenerating.value = true
  generationError.value = null

  try {
    const result = await api.generateCoverLetter(jobDescription.value, userInput.value)
    generatedCoverLetter.value = result
  } catch (error) {
    generationError.value = error.message || 'Failed to generate cover letter'
    console.error('Cover letter generation error:', error)
  } finally {
    isGenerating.value = false
  }
}

// Skills form and list
const skillForm = useItemForm({
  apiAddFunction: api.addSkill,
  piniaAddFunction: skillStore.piniaAddSkill,
  inputProperty: 'skill',
  validationErrorMessage: 'Invalid input: skill is either empty or not a string.'
})

const skillList = useItemList({
  apiGetFunction: api.getSkills,
  apiDeleteFunction: api.deleteSkill,
  piniaStore: skillStore,
  piniaDeleteFunction: skillStore.piniaDeleteSkill,
  listProperty: 'skillSetList',
  itemKey: 'item'
})

// Words form and list
const wordsForm = useItemForm({
  apiAddFunction: api.addWord,
  piniaAddFunction: wordsStore.piniaAddWord,
  inputProperty: 'word',
  validationErrorMessage: 'Invalid input: word is either empty or not a string.'
})

const wordsList = useItemList({
  apiGetFunction: api.getWords,
  apiDeleteFunction: api.deleteWord,
  piniaStore: wordsStore,
  piniaDeleteFunction: wordsStore.piniaDeleteWord,
  listProperty: 'removeWordsList',
  itemKey: 'item'
})

// Sentences form and list
const sentencesForm = useItemForm({
  apiAddFunction: api.addSentence,
  piniaAddFunction: sentencesStore.piniaAddSentence,
  inputProperty: 'sentence',
  validationErrorMessage: 'Invalid input: sentence is either empty or not a string.'
})

const sentencesList = useItemList({
  apiGetFunction: api.getSentences,
  apiDeleteFunction: api.deleteSentence,
  piniaStore: sentencesStore,
  piniaDeleteFunction: sentencesStore.piniaDeleteSentence,
  listProperty: 'removeSentencesList',
  itemKey: 'item'
})
</script>

<template>
    <div>
        <v-container id = "jobsearch-header">
    <!-- Debug info -->

            <v-row>
                <div class="jobsearch">
                    <h1>Job market, the search</h1>
                    <v-sheet>
                        When generating job applications or professional documents using a language model, certain words or phrases can be omitted or rephrased to leverage the model's auto-corrective capabilities. By creating a list of terms to avoid, you can guide the model to produce more consistent and professional results. However, it's essential not to overload this list, as too many constraints can reduce the model's effectiveness.
                        LLMs have limitations in how many corrections they can handle in a single call. When the number of corrections exceeds a certain threshold, the quality of self-correction can deteriorate, leading to less coherent responses. For optimal results, keep the list of forbidden words to a manageable size, allowing the model to balance its adaptive capabilities while maintaining output quality.
                    </v-sheet>
                </div>
            </v-row>
        
            <v-row>
                <v-col cols="12">
                    <v-sheet>
                        <v-card-title>Job market analysis</v-card-title>
                        <v-card-text>

                        </v-card-text>
                    </v-sheet>
                </v-col>
            </v-row>
        </v-container>

        <v-container class ="job-listing-container mb-4">
            <!-- JOBLISTINGS Container -->
            <v-row justify="space-between">
            <!-- Column 1: Contains the First Card -->
                <v-col cols="12">
                    <v-card-title>Data table for listings</v-card-title>
                    <v-card-text>
                    Select one or multiple positions of interest, for semi-generated applications with human-in-the-loop.
                    <br>
                    Info: Click on Description to view the full text or click the link for redirection to the job listing.    
                    </v-card-text>
                    <!-- <JobListings /> -->
                </v-col>               
            </v-row>
        </v-container>

        <v-container class="cover-letter-container mb-4">
            <!-- COVER LETTER Container -->
            <v-row >
                <!-- Column 1: Contains the First Card -->
                <v-col cols="12">
                    <v-sheet>
                        <h3>Upload templates for a cover latter.</h3>
                        <p>The template can currently be in the format of .txt or .pdf format</p>
                        <p>The file will be saved. The text inside the file will be extracted and used as input to generate a cover letter</p>
                        <p>It is advised, to have at least 5 different templates for different positions.</p>
                        <p>Furthermore, add one file at a time in order to control and validate, that the extracted text is correct and in the rightfull order</p>
                        <FileUploads/>
                    </v-sheet>
                </v-col>                   
            </v-row>


        </v-container>

         <v-container class="users-unique-skillset-container mb-4">
            <!-- SKILL Container -->
            <!-- First Row: Description and Input -->
            <v-row >
                <v-col cols="8">
                    <v-card-title>Add/Remove unique skills</v-card-title>
                    <v-card-text>
                        <p>You can add & remove unique skills or traits that you possess. This will map your competencies with those of the required position that being targeted.</p>
                        <p>E.g. if you are appling for a software developer position, you can add skills like "Python", "Java", "C++", etc.</p>                        
                        <p>The idea is to help the model understand your unique skills and traits, and generate a more personalized application.</p>
                        <p>It also serves as a grounding to minimize a models tendency hallucinate or confabulations of information in regard to your trustworthiness.</p>
                    </v-card-text>
                </v-col>
                <v-col cols="4" class="d-flex align-center">
                    <form @submit.prevent="skillForm.addItemAndClear" class="w-100">
                        <v-text-field
                            v-model="skillForm.item.skill"
                            label="Add your skill"
                            class="mb-3"
                        />
                        <v-btn type="submit" color="primary" block>Add</v-btn>
                    </form>
                </v-col>
            </v-row>
            
            <!-- Second Row: Skills List -->
            <v-row class="mt-n8">
                <v-col cols="12">
                    <v-list v-if="skillList.items?.value && skillList.items.value.length > 0" class="d-flex flex-wrap">
                        <v-chip
                            v-for="skill in skillList.items.value" 
                            :key="skill?.id || Math.random()"
                            class="ma-1"
                            closable
                            @click:close="skillList.deleteItem(skill?.id)"
                        >
                            {{ skill.text }}
                        </v-chip>
                    </v-list>
                    <v-alert v-else type="info" variant="tonal">
                        No skills loaded yet. Add a skill to get started.
                    </v-alert>
                </v-col>
            </v-row>
        </v-container>


        <v-container class="words-removal-container mb-4">
            <!-- First Row: Description and Input -->
            <v-row>
                <v-col cols="8">
                    <v-card-title>Auto-correct words</v-card-title>
                    <v-card-text>
                        <p>Enter unique words in the input box on the right and click "Add" to exclude them.</p>
                        <p>You can also remove any words from the list by clicking.</p>
                        <p>We apply auto-correction of certain words be telling the LLM to look for them.</p>
                        <p>These restrictstions is meant to support our lazyness in writing application, meaning that we are less likely to sound like a LLM-Agent</p>
                    </v-card-text>
                </v-col>
                <v-col cols="4" class="d-flex align-center">
                    <form @submit.prevent="wordsForm.addItemAndClear" class="w-100">
                        <v-text-field
                            v-model="wordsForm.item.word"
                            label="Add invalid words"
                            class="mb-3"
                        />
                        <v-btn type="submit" color="primary" block>Add</v-btn>
                    </form>
                </v-col>
            </v-row>

            <!-- Second Row: Words List -->
            <v-row class="mt-n8">
                <v-col cols="12">
                    <v-list v-if="wordsList.items?.value && wordsList.items.value.length > 0" class="d-flex flex-wrap">
                        <v-chip
                            v-for="word in wordsList.items.value" 
                            :key="word?.id || Math.random()"
                            class="ma-1"
                            closable
                            @click:close="wordsList.deleteItem(word?.id)"
                        >
                            {{ word.text }}
                        </v-chip>
                    </v-list>
                    <v-alert v-else type="info" variant="tonal">
                        No words added yet. Add a word to get started.
                    </v-alert>
                </v-col>
            </v-row>
        </v-container>



        <v-container class = "phrase-removal-container mb-4">
            <!-- First Row: Description and Input -->
            <v-row>
                <v-col cols="8">
                    <v-card-title>Auto-correct sentences & phrases</v-card-title>
                    <v-card-text>
                        <p>Enter unique sentences in the input box on the right and click "Add" to exclude them.</p>
                        <p>If you have experiences that the LLM-Agents continuesly generate phrases or sentences that are less attractive, these guardrails serves to mitigate such scenarios</p>
                    </v-card-text>
                </v-col>
                <v-col cols="4" class="d-flex align-center">
                    <form @submit.prevent="sentencesForm.addItemAndClear" class="w-100">
                        <v-text-field
                            v-model="sentencesForm.item.sentence"
                            label="Add invalid sentences/phrases"
                            class="mb-3"
                        />
                        <v-btn type="submit" color="primary" block>Add</v-btn>
                    </form>
                </v-col>
            </v-row>

            <!-- Second Row: Sentences List -->
            <v-row class="mt-n8">
                <v-col cols="12">
                    <v-list v-if="sentencesList.items?.value && sentencesList.items.value.length > 0" class="d-flex flex-wrap">
                        <v-chip
                            v-for="sentence in sentencesList.items.value" 
                            :key="sentence?.id || Math.random()"
                            class="ma-1"
                            closable
                            @click:close="sentencesList.deleteItem(sentence?.id)"
                        >
                            {{ sentence.text }}
                        </v-chip>
                    </v-list>
                    <v-alert v-else type="info" variant="tonal">
                        No sentences added yet. Add a sentence to get started.
                    </v-alert>
                </v-col>
            </v-row>
        </v-container>

        <v-container class="cover-letter-layout mb-4">
            <!-- INPUT SECTION -->
            <v-row>
                <v-col cols="12">
                    <v-card>
                        <v-card-title>Generate Cover Letter</v-card-title>
                        <v-card-text>
                            <p class="mb-4">Paste the job description below and optionally add personal notes. The agent will generate a tailored cover letter using your skills, templates, and preferences.</p>

                            <v-textarea
                                v-model="jobDescription"
                                label="Job Description *"
                                placeholder="Paste the full job description here..."
                                rows="8"
                                variant="outlined"
                                class="mb-4"
                            />

                            <v-textarea
                                v-model="userInput"
                                label="Personal Notes (Optional)"
                                placeholder="Add any personal notes or specific points you want to highlight..."
                                rows="3"
                                variant="outlined"
                                class="mb-4"
                            />

                            <v-alert v-if="generationError" type="error" class="mb-4">
                                {{ generationError }}
                            </v-alert>

                            <v-btn
                                color="primary"
                                size="large"
                                :loading="isGenerating"
                                :disabled="!jobDescription.trim()"
                                @click="generateCoverLetter"
                            >
                                <v-icon left>mdi-robot</v-icon>
                                Generate Cover Letter
                            </v-btn>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>

            <!-- OUTPUT SECTION -->
            <v-row v-if="generatedCoverLetter" class="mt-4">
                <v-col cols="12">
                    <v-card>
                    <span>test</span>
                        <v-card-title class="d-flex justify-space-between align-center">
                            <span>Generated Cover Letter</span>
                            <v-chip color="success">
                                {{ generatedCoverLetter.iterations }} iterations | {{ generatedCoverLetter.violations }} violations
                            </v-chip>
                        </v-card-title>
                        <v-card-text>
                            <div class="cover-letter-content">
                                <div class="mb-4">
                                    <strong>{{ generatedCoverLetter.company_name }}</strong><br>
                                    <strong>{{ generatedCoverLetter.job_title }}</strong>
                                </div>

                                <div class="mb-4">
                                    <h4 class="text-subtitle-1 font-weight-bold mb-2">Introduction</h4>
                                    <p class="text-body-1">{{ generatedCoverLetter.introduction }}</p>
                                </div>

                                <div class="mb-4">
                                    <h4 class="text-subtitle-1 font-weight-bold mb-2">Motivation</h4>
                                    <p class="text-body-1">{{ generatedCoverLetter.motivation }}</p>
                                </div>

                                <div class="mb-4">
                                    <h4 class="text-subtitle-1 font-weight-bold mb-2">Unique Selling Points</h4>
                                    <p class="text-body-1">{{ generatedCoverLetter.unique_selling_points }}</p>
                                </div>

                                <div class="mb-4">
                                    <h4 class="text-subtitle-1 font-weight-bold mb-2">Key Highlights</h4>
                                    <p class="text-body-1 ml-4">• {{ generatedCoverLetter.bulletpoint_1 }}</p>
                                    <p class="text-body-1 ml-4">• {{ generatedCoverLetter.bulletpoint_2 }}</p>
                                    <p class="text-body-1 ml-4">• {{ generatedCoverLetter.bulletpoint_3 }}</p>
                                    <p class="text-body-1 ml-4">• {{ generatedCoverLetter.bulletpoint_4 }}</p>
                                </div>

                                <div>
                                    <h4 class="text-subtitle-1 font-weight-bold mb-2">Thank You</h4>
                                    <p class="text-body-1">{{ generatedCoverLetter.thank_you }}</p>
                                </div>
                            </div>

                            <v-divider class="my-4" />

                            <div class="text-center">
                                <v-btn color="secondary" variant="outlined" class="mr-2">
                                    <v-icon left>mdi-download</v-icon>
                                    Download PDF
                                </v-btn>
                                <v-btn color="primary" variant="outlined">
                                    <v-icon left>mdi-content-copy</v-icon>
                                    Copy to Clipboard
                                </v-btn>
                            </div>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>
  
  <style>
.job-listing-component {
    /*border: 1px solid #ddd; /* Optional: Border to see the container's boundaries */
    height: 200; /* Set the max height of the container */
 }

.users-unique-skillset-container {
    border: 1px solid #ddd; /* Optional: Border to see the container's boundaries */
    height: 150; /* Set the max height of the container */
    overflow-y: auto; /* Enable vertical scrolling if content exceeds max height */
    padding-bottom: 16px;    
}

.words-removal-container {
     border: 1px solid #ddd; /* Optional: Border to see the container's boundaries */
     height: 150; /* Set the max height of the container */
     overflow-y: auto; /* Enable vertical scrolling if content exceeds max height */
     padding-bottom: 16px;
}

.phrase-removal-container {
     border: 1px solid #ddd; /* Optional: Border to see the container's boundaries */
     height: 150; /* Set the max height for the #wordsList container */
     overflow-y: auto; /* Enable vertical scrolling if content exceeds max height */
     padding: 16px; /* Optional: Padding inside the container */
}

.cover-letter-content {
    line-height: 1.8;
    max-width: 800px;
    margin: 0 auto;
}

.cover-letter-content p {
    white-space: pre-wrap;
    word-wrap: break-word;
}

  </style>
  