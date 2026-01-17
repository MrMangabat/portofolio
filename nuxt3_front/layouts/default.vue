<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>RealUnicorns</v-toolbar-title>
      <v-spacer />
      <v-btn nuxt to="/">Home</v-btn>

      <!-- Projects Dropdown Menu -->
      <v-menu open-on-hover offset-y>
        <template #activator="{ props }">
          <v-btn text v-bind="props">
            Projects
            <v-icon right>mdi-menu-down</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item nuxt to="/jobsearch/JobSearch">
            <v-list-item-title>Job Search</v-list-item-title>
          </v-list-item>
          <v-list-item nuxt to="/TimeSeriesAnalysis">
            <v-list-item-title>Time Series Analysis</v-list-item-title>
          </v-list-item>
          <v-list-item nuxt to="/OSINT">
            <v-list-item-title>OSINT</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <!-- Nested Menu for “Personal Trainer” -->
      <v-menu open-on-hover offset-y>
        <template #activator="{ props }">
          <v-btn text v-bind="props">
            Personal Trainer
            <v-icon right>mdi-menu-down</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item nuxt to="/training-progression">
            <v-list-item-title>Training Progression</v-list-item-title>
          </v-list-item>
          <v-list-item nuxt to="/program-generation">
            <v-list-item-title>Program Generation</v-list-item-title>
          </v-list-item>
          <v-list-item nuxt to="/exercise-library">
            <v-list-item-title>Exercise Library</v-list-item-title>
          </v-list-item>
          <v-list-item nuxt to="/pricing">
            <v-list-item-title>Pricing</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn text to="/pricing">Bartending</v-btn>
      <v-btn text to="/contact">Contact</v-btn>
      <v-btn text to="/profile">Profile</v-btn>
      <v-btn text to="/login">Screening</v-btn>
    </v-app-bar>

    <v-main>
      <slot/>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
// Default layout with toolbar across all pages
</script>