<script setup>
  import { RouterLink, RouterView } from 'vue-router'
  import { ref } from 'vue'

  const showTopics = ref(false)



</script>

<template>
  <!-- nav bar -->
  <v-layout id="app" class="rounded rounded-md">  
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>To those who got lost and ended here, I salute</v-toolbar-title>
      
      <v-btn 
        text to="/projects"> Projects 
      </v-btn>

      <v-menu v-model="showTopics" transition="slide-y-transition">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props">
            Topics of Interests
          </v-btn>
        </template>

        <v-list>
          <v-list-item>
            <v-list-item-title>
              <v-btn text to="/knowledge-engineering">Knowledge Engineering?</v-btn>
            </v-list-item-title>

            <v-list-item-title>
              <v-btn text to="/natural-language-processing">Natural Language Processing</v-btn>
            </v-list-item-title>

            <v-list-item-title>
              <v-btn text to="/random-stuff">Some random stuff</v-btn>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      


      <v-btn
        text to="/cvandstuff"> CV + stuff
      </v-btn>

      <v-btn 
        text to="/about"> About 
      </v-btn>

      <!-- <v-btn 
        text to="/login"> Login
      </v-btn> -->

    </v-app-bar>   

    <v-container>
      <v-main 
        class="d-flex align-center justify-center" 
        style="min-height: 300px;">
        <router-view></router-view>
      </v-main>
    </v-container>
    
  </v-layout>
</template>

<style> /*scoped = unique style for this component*/
#layout {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
/* gloabal css styling  */
/* setting navigation padding  */
nav {
  padding: 30px;
}
/* setting nav a  */
nav a {
  font-weight: bold;
  color: #2c3e50;
}
nav a.router-link-exact-active {
  color: #42b983;
}
/* setting h2 font size   */
h2 {
  font-size: 20px;
}
</style>
