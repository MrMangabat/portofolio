<script setup>

import TimeLine from '../components/TimeLine.vue'
import EducationLine from '../components/EducationLine.vue'

</script>


<template>
  <v-container id = "about">
    <div>
      <h1 style="display: flex; justify-content: center;">By all means, this is just a personal space where I look into topics of interest.</h1>
      <br>

      <p>
        <h2>Hello stranger, thanks for the peek!</h2> 
        <br>
        This space is my digital playground - a melting pot of ideas and experimentsin the dynamic realms of software engineering, project development, and artificial intelligence.
        As I navigate through the paths of my professional journey, which has just begun as i graduated the summer of 2023 with a masters degree in data science ICT. This site serves as a chronicle of my growth, curiousity and explorations.
        The gist lies in the fascinating world of information technology. It's here that I delve into the excitement of these technologies, unraveling their potentials and applying them to real-world scenarios as I explore more.
      </p>
      <br>

      <h2>A Glimpse into My World of Interests</h2>
      <p>
        My academic and professional pursuits are  rooted in the fields of macroeconomics, software development/engineering & data science, specifically interested in natural language processing, and the broader of knowledge engineering.
        I am passionately curious about how we can extract meaningful insights from the unstructured data that surrounds us - be it text, videos, or images.
        The challenge of deciphering this data and transforming it into actionable knowledge is what drives me.
      </p>
      <br>

      <h2>Journey Through Interrsting Research and Learning</h2>
      <p>
        In this ever-evolving journey, I am committed to continuous learning and sharing. This site will feature updates on insightful papers I've found interesting or simply do not understand at all supplemented by key takeaways from my explorations.
        Look out for updates in the research banner, since it will become a recommendation system according to my preferred subjects as well as projects where I’ll be sharing these nuggets of knowledge and new experiences.
      </p>
      <br>

      <h2>Collaboration & sharing</h2>
      <p>
        I believe in the power of community-driven development and the sharing of knowledge.
        You can view the structure, documentation, and progress of what you are seeing on my <a href="https://github.com/MrMangabat/portofolio">GitHub</a>. Feel free to explore, contribute, or provide feedback.
      </p>
      <br>

      <p>
        Feel free to connect and ollaborate or even better, provide contructive feedback as I continue to grow and evolve in this exciting field.
        Whether you're a fellow enthusiast, a curious geek, or a potential collaborator, let's connect and explore ideas of the endless possibilities that the future of technology holds.
        Thank you for stopping by, and I look forward to sharing this journey with you!
      <br>
      <br>
        By the way, if you find this interesting and need a new collegue, hit me up as i am currently looking for a full time job since I recently gradudated.
      </p>
      <br>
    </div>

    <v-row >
      <h2> row 1 </h2>
      <v-col>
        <h3>kol 1</h3>

        
        <v-card>
          <h2 style="display: flex; justify-content: center;">Education</h2>
          
          <EducationLine/>
        </v-card>
      </v-col>

      <v-col>
        <h3>kol 2</h3>
        <v-card 
          width="1000px"
          class="mx-auto"
        >
        <h2 style="display: flex; justify-content: center;">Working experiences</h2>
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
