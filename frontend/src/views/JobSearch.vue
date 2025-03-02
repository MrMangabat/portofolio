<script setup>
import WordsForm from '../components/jobsearch_view/WordsForm.vue';
import WordsList from '../components/jobsearch_view/WordsList.vue';
import SentencesForm from '../components/jobsearch_view/SentenceForm.vue';
import SentenceList from '../components/jobsearch_view/SentenceList.vue';
import SkillsetForm from '../components/jobsearch_view/SkillsetForm.vue';
import SkillSetList from '../components/jobsearch_view/SkillSetList.vue';
import JobListings from '../components/jobsearch_view/JobListings.vue';
import FileUploads from '../components/jobsearch_view/FileUploads.vue';


</script>

<template>
    <div>
        <v-container id = "jobsearch-header">
            <v-row>
                <div class="jobsearch">
                    <h1>Job market, the search</h1>
                    <v-sheet>
                        When generating job applications or professional documents using a language model, certain words or phrases can be omitted or rephrased to leverage the model's auto-corrective capabilities. By creating a list of terms to avoid, you can guide the model to produce more consistent and professional results. However, it’s essential not to overload this list, as too many constraints can reduce the model’s effectiveness.
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
                    <v-card-title>data table for listings</v-card-title>
                    <v-card-text>
                    Select one or multiple positions of interest, for semi-generated applications with human-in-the-loop.
                    <br>
                    Info: Click on Description to view the full text or click the link for redirection to the job listing.    
                    </v-card-text>
                    <JobListings />
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
            <v-row>
            <!-- Column 1: Contains the First Card -->
                <v-col cols="4">
                    <v-card-title>Add/Remove unique skills</v-card-title>
                    <v-card-text>
                        <p>You can add & remove unique skills or traits that you possess. This will map your competencies with those of the required position that being targeted.</p>
                        <p>E.g. if you are appling for a software developer position, you can add skills like "Python", "Java", "C++", etc.</p>                        
                        <p>The idea is to help the model understand your unique skills and traits, and generate a more personalized application.</p>
                        <p>It also serves as a grounding to minimize a models tendency hallucinate or confabulations of information in regard to your trustworthiness.</p>
                    </v-card-text>
                </v-col>
                <!-- Center: Input Field and Button in the Same Column -->
                <v-col cols="3">
                    <SkillsetForm/>
                </v-col>
                

                <!-- Column 2: Contains the WordsList Component -->
                <v-col cols="5">
                    <SkillSetList />
                </v-col>
            </v-row>
        </v-container>


        <v-container class="words-removal-container mb-4">
            <!-- Main Row Container with 12 Columns Split -->
            <v-row>
                <!-- Left Side: Description Text -->
                <v-col cols="4">
                    <v-card-title>Auto-correct words</v-card-title>
                    <v-card-text>
                        <p>Enter unique words in the input box on the right and click "Add" to exclude them.</p>
                        <p>You can also remove any words from the list by clicking.</p>
                        <p>We apply auto-correction of certain words be telling the LLM to look for them.</p>
                        <p>These restrictstions is meant to support our lazyness in writing application, meaning that we are less likely to sound like a LLM-Agent</p>
                    </v-card-text>
                </v-col>

                <!-- Center: Input Field and Button in the Same Column -->
                <v-col cols="3">
                    <WordsForm/>
                </v-col>

                <!-- Right Side: Skill List -->
                <v-col cols="5">
                    <WordsList />
                </v-col>
            </v-row>
        </v-container>



        <v-container class = "phrase-removal-container mb-4">
            <!-- Main Row Container with 12 Columns Split -->
            <v-row>
                <!-- Left Side: Description Text -->
                <v-col cols="4">
                    <v-card-title>Auto-correct sentences & phrases</v-card-title>
                    <v-card-text>
                        <p>Enter unique sentences in the input box on the right and click "Add" to exclude them.</p>
                        <p>If you have experiences that the LLM-Agents continuesly generate phrases or sentences that are less attractive, these guardrails serves to mitigate such scenarios</p>
                    </v-card-text>
                </v-col>

                <!-- Center: Input Field and Button in the Same Column -->
                <v-col cols="3">
                    <SentencesForm/>
                </v-col>

                <!-- Right Side: Skill List -->
                <v-col cols="5">
                    <SentenceList />
                </v-col>
            </v-row>
        </v-container>

        <v-container class ="cover-letter-layout">
            <row>
                <v-col>
                    <v-card-title>Generated Cover Letter</v-card-title>
                    <v-card-text>
                        <p>Generated cover letter based on the input text and the job listings selected.</p>
                        <p>Click on the "Generate Cover Letter" button to generate a cover letter.</p>
                        <p>Click on the "Download Cover Letter" button to download the generated cover letter.</p>
                    </v-card-text>
                </v-col>
            </row>
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


  </style>
  