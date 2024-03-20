<script setup>

import TimeLine from '../components/TimeLine.vue'
import EducationLine from '../components/EducationLine.vue'

</script>


<template>
    <v-container 
        id = "CVandExperiences">
        
            <v-row 
                id="1stRow">
                <v-col 
                    cols="2" 
                    id="introtext">
                    
                </v-col>

                <v-col 
                    cols="8">
                    <div>
                        <h1 style="display: flex; justify-content: center;"> Professional Aspiration </h1>
                        <br>

                        <p>
                            This page serves as a snapshot of my academic journey, professional experiences, and certifications. 
                            My ambition is to carve a path as an AI Engineer specializing in knowledge enigneering, data, and process mining, coupled with Natural Language Processing (NLP).
                            I firmly believe that the bedrock of successful AI implementations lies in a deep understanding of data, business imperatives, legal frameworks, and the capacity to deliver tangible value to clients through technology.
                            In essence, I aspire to become a full-stack AI/ML Engineer.
                        </p>
                        <br>

                        <h2 style="display: flex; justify-content: center;"> Masters thesis </h2>
                        <p>
                            I recently completed my Master's degree in Data Science ICT, where my thesis delved into leveraging foundational transformer models (RoBERTa, BERT, FinBERT, T5) for semi-automated PEST analysis generation.
                            This involved employing Named Entity Recognition and summarization techniques on publicly available data to furnish a macroeconomic overview pertinent to market expansion endeavors. 
                            The core objective was to distill insights from vectorized unstructured data by generating summaries and retrieving relevant information based on semantic similarity and ranking derived from the foundational models.

                        </p>
                        <br>

                        <h2 style="display: flex; justify-content: center;"> Bachelor thesis </h2>
                        <p>
                            Complementing my graduate studies, I hold a Professional Bachelor's Degree in Economics & IT. 
                            My undergraduate thesis centered on Enterprise Architecture as a strategic imperative for EnviroProcess Denmark and its parent company, EnviroProcess AB. 
                            The objective was to devise an IT strategy aligned with the subsidiary's core competencies and industry-specific knowledge, ensuring seamless integration and optimal utilization of resources.
                        </p>
                        <br>

                        <h2 style="display: flex; justify-content: center;"> Motivation </h2>
                        <p>
                            My commitment to staying abreast of the latest advancements in AI is unwavering.
                            I devote considerable time to studying cutting-edge research, particularly focusing on multi-agent learning frameworks, self-reflective RAG, and knowledge mining/engineering for enhanced decision-making and knowledge retention.
                            I draw inspiration from thought leaders such as Cassie Kozyrkov, particularly in the realm of decision intelligence.
                        </p>
                        <br>

                        <h2 style="display: flex; justify-content: center;"> Skills </h2>
                        <p>
                            My professional journey has endowed me with robust communication skills honed over years in the hospitality industry, spanning diverse environments ranging from standard to luxury establishments.
                            These experiences have empowered me to bridge the chasm between business value propositions and the fundamental requirements essential for AI or software solution implementation.
                            I am characterized by thoughtfulness and an inclination towards sustainable, long-term solutions.
                            I am unafraid to question the status quo or offer constructive feedback to enrich dialogues and ensure alignment with stakeholders.
                            Diligence, high motivation, and unwavering perseverance are integral facets of my work ethic.
                        </p>
                    </div>
                </v-col>

                <v-col cols="2">

                </v-col>
            </v-row>

            <v-row id="2ndRow">
                <v-col cols="2">
                
                </v-col>

                <v-col cols="4">
                    <v-card>
                        <v-card>
                        <v-card-title style="display: flex; justify-content: center;">Certificates</v-card-title>
                        <v-card-body>
                            <v-row>
                                <v-col>
                                    <v-card>
                                        <v-card-title>Python</v-card-title>
                                        <v-card-text>
                                            <v-img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" aspect-ratio="2.75"></v-img>
                                        </v-card-text>
                                    </v-card>
                                </v-col>
                            </v-row>
                        </v-card-body>
                        

                        
                        <v-card-title>Courses</v-card-title>

                            dsad
                        </v-card>
                    </v-card>
                </v-col>

                <v-col cols="4">
    
                    <div>
                        <v-card width="660px">
                            <h2 style="display: flex; justify-content: center;">Education</h2>
                            <EducationLine/>
                        </v-card>
                    </div>
                </v-col>

                <v-col cols="2">
                    4
                </v-col>
            </v-row>
        <v-row
            id = "3rdRow">
            <v-col 
                cols="2"
                id = "..">

            </v-col>

            <v-col 
                cols="8">
                <div>
                    2
                    <v-card 
                    width="1500px"
                    class="mx-auto">
            
                    <h2 style="display: flex; justify-content: center;">Working experiences</h2>
                    <v-card-text style="overflow-y: auto;">
                        <TimeLine />
                    </v-card-text>
                    </v-card>
                </div>
            </v-col>
            
            <v-col 
                cols="2">
            </v-col>
        </v-row>


    </v-container>
</template>

<style>

</style>