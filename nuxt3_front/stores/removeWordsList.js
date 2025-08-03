// frontend/src/stores/removeWordsList.js

import { defineStore } from 'pinia';

export const useRemoveWordsList = defineStore('removeWordsList', {
  state: () => ({
    removeWordsList: [],
  }),
  actions: {
    piniaAddWord(wordData) {
      this.removeWordsList.push({
        id: wordData.id,
        text: wordData.text,
        type: wordData.type,
        completed: false,
      });
    },
    piniaDeleteWord(wordId) {
      this.removeWordsList = this.removeWordsList.filter((object) => object.id !== wordId);
    },
  },
});
