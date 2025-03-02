// frontend/src/stores/removeSentenceList.js

import { defineStore } from 'pinia';

export const useRemoveSentencesList = defineStore('removeSentencesList', {
  state: () => ({
    removeSentencesList: [],
  }),
  actions: {
    piniaAddSentence(sentenceData) {
      this.removeSentencesList.push({
        id: sentenceData.id,
        item: sentenceData.text,
        completed: false,
      });
    },
    piniaDeleteSentence(sentenceId) {
      this.removeSentencesList = this.removeSentencesList.filter(
        (object) => object.id !== sentenceId
      );
    },
  },
});
