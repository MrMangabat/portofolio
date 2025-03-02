<!-- frontend/src/components/jobsearch_view/WordsList.vue -->

<script setup>
import { useItemList } from '@/composables/useItemList';
import jobsearch_api from '../../apis/jobsearch_api';
import { useRemoveWordsList } from '@/stores/removeWordsList';

const store = useRemoveWordsList();

const { items, deleteItem } = useItemList({
  apiGetFunction: jobsearch_api.getWords,
  apiDeleteFunction: jobsearch_api.deleteWord,
  piniaStore: store,
  piniaDeleteFunction: store.piniaDeleteWord.bind(store),
  listProperty: 'removeWordsList',
  itemKey: 'item',
});
</script>

<template>
  <v-container class="remove-words-list-component">
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-text>
            <div class="word-item-container">
              <v-chip
                v-for="word in items"
                :key="word.id"
                @click="deleteItem(word.id)"
                close
                class="item">
                {{ word.item }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.remove-words-list-component {
  height: 250px;
  overflow-y: auto;
}

.word-item-container {
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