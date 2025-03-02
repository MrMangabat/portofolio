<script setup>
import { RouterLink, RouterView } from 'vue-router'
import JobSearch from './views/JobSearch.vue';
</script>

<template>

  <!-- nav bar -->
  <v-layout id ='app' class="rounded rounded-md">  
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Jannik M. B. Sørensen</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn 
        text 
        to = "/projectsoverview"> Projects </v-btn>
        <!-- <router-link to="/projectoverview">Projects</router-link> -->

      <v-btn 
        text 
        to = "/about"> About </v-btn>

      <v-btn 
        text
        to = "/Research"> Interesting articels </v-btn>

      <v-btn
        text
        to = "/login"> Login </v-btn>
    </v-app-bar>   
    
    <v-container>
      <v-main 
        class = "d-flex align-center justify-center" 
        style = "min-height: 300px;">
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
