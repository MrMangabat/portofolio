<!-- frontend/src/components/jobsearch_view/SkillSetList.vue -->

<script setup>
import { useItemList } from '@/composables/useItemList';
import jobsearch_api from '../../apis/jobsearch_api';
import { useSkillset } from '@/stores/skillSetStore';

const store = useSkillset();

const { items, deleteItem } = useItemList({
  apiGetFunction: jobsearch_api.getSkills,
  apiDeleteFunction: jobsearch_api.deleteSkill,
  piniaStore: store,
  piniaDeleteFunction: store.piniaDeleteSkill.bind(store),
  listProperty: 'skillSetList',
  itemKey: 'item',
});
</script>

<template>
  <v-container class="skill-list-component">
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-text>
            <div class="skill-chips-container">
              <v-chip
                v-for="skill in items"
                :key="skill.id"
                @click="deleteItem(skill.id)"
                close
                class="mx-1 my-1">
                {{ skill.item }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.skill-list-component {
  height: 250px;
  overflow-y: auto;
}

.item-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.item {
  cursor: pointer;
  padding: 4px 8px;
  background-color: #e0f7fa; /* Light cyan background */
  border-radius: 4px;
  white-space: nowrap;
  
}
</style>
