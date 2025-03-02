<!-- frontend/src/components/jobsearch_view/SentenceList.vue -->

<script setup>
import { useItemList } from '@/composables/useItemList';
import jobsearch_api from '../../apis/jobsearch_api';
import { useRemoveSentencesList } from '@/stores/removeSentencesList';

const store = useRemoveSentencesList();

const { items, deleteItem } = useItemList({
  apiGetFunction: jobsearch_api.getSentences,
  apiDeleteFunction: jobsearch_api.deleteSentence,
  piniaStore: store,
  piniaDeleteFunction: store.piniaDeleteSentence.bind(store), // Bind the action
  listProperty: 'removeSentencesList',
  itemKey: 'item',
});

</script>

<template>
  <v-container class="remove-sentences-list-component">
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-text>
            <div class="sentence-chips-container">
              <v-chip
                v-for="sentence in items"
                :key="sentence.id"
                @click="deleteItem(sentence.id)"
                class="item">
                {{ sentence.item }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.remove-sentences-list-component {
  height: 250px;
  overflow-y: auto;
}

.sentence-chips-container {
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