<script setup>
import TimeLine from '../components/TimeLine.vue'
import EducationLine from '../components/EducationLine.vue'
</script>


<template>
  <v-container id = "about">
    <h1 align = "center"> Welcome to my world of exploration and discovery

</h1>
      <div>
        <v-card>
            <v-card-title></v-card-title>
            <v-card-body >
              <v-card-text class = "about">
                Welcome. This is just me exploring things i find interesting and trying out different things related to analysis and AI & Machine Learning.

Hello, and thank you for visiting! My name is Jannik , and this space is my digital playground - a melting pot of ideas, experiments, and breakthroughs in the dynamic realms of software engineering, project development, and artificial intelligence.
As I navigate through the intricate paths of my professional journey, which has just begun as i graduated the summer of 2023 with a masters degree in data science ICT.  This site serves as a living chronicle of my growth, curiousity and explorations.
The heart of my work lies in the fascinating world of machine learning and deep learning. It's here that I delve into the excitement of these technologies, unraveling their potentials and applying them to real-world scenarios.

A Glimpse into My World of Interests
My academic and professional pursuits are deeply rooted in the fields of macroeconomics, software development/engineering, natural language processing, and the broader spectrum of business intelligence.
I am passionately curious about how we can extract meaningful insights from the unstructured data that surrounds us - be it text, videos, or images.
The challenge of deciphering this data and transforming it into actionable knowledge is what drives me.

Journey Through Research and Learning
In this ever-evolving journey, I am committed to continuous learning and sharing. This site will regularly feature updates on intriguing research topics, insightful papers I've encountered, and key takeaways from my explorations.
Look out for updates in the research banner, since it will become a recommendation system according to my preferred subjects as well as projects where I’ll be sharing these nuggets of knowledge and new experiences.

Open Source - A Commitment to Community and Collaboration
In my quest for knowledge, I am a staunch advocate for open source software. I believe in the power of community-driven development and the sharing of knowledge.
You can view the structure, documentation, and progress of my projects on my GitHub account. Feel free to explore, contribute, or provide feedback.

Connect and Collaborate
As I continue to grow and evolve in this exciting field, I invite you to join me on this journey.
Whether you're a fellow enthusiast, a curious learner, or a potential collaborator, let's connect and explore the endless possibilities that the future of technology holds.
Thank you for stopping by, and I look forward to sharing this journey with you! By the, if you find this interesting and need a new collegue, hit me up as i am currently looking for a full time job since I recently gradudated.
              </v-card-text>
            </v-card-body>
        </v-card>        
      </div>
    <v-row >
      <h2> row 1 </h2>
      <v-col>
        <h3>kol 1</h3>

        
        <v-card>
          <h2 align = "center">Education</h2>
          <EducationLine />
        </v-card>
      </v-col>

      <v-col>
        <h3>kol 2</h3>
        <v-card 
          width="1000px"
          class="mx-auto"
        >
          <h2 align="center">Working Experiences</h2>
          <v-card-text style="overflow-y: auto;">
            <TimeLine />
          </v-card-text>
        </v-card>

      </v-col>
  
    </v-row>
<!-- 
    <v-row>
      <h2> row 2 </h2>
      <v-col>
        <h3>kol 1</h3>
        <v-card>
          <v-card-title>Certificates</v-card-title>
          <v-card-body>ds</v-card-body>
        </v-card>
      </v-col>
    </v-row> -->

 

  </v-container>
</template>

<style scoped>
  .about {
   
    padding: 20px;
    height : 100px;
    width: 300px;
  }
  

</style>
