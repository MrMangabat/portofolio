// frontend/src/stores/skillSetStore.js

import { defineStore } from 'pinia';

export const useSkillset = defineStore('skillSets', {
  state: () => ({
    skillSetList: [],
  }),
  actions: {
    piniaAddSkill(skillData) {
      this.skillSetList.push({
        id: skillData.id,
        item: skillData.text, // Ensure this matches the data structure
        completed: false,
      });
    },
    piniaDeleteSkill(skillId) {
      this.skillSetList = this.skillSetList.filter((object) => object.id !== skillId);
    },
  },
});