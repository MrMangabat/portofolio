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
        text: skillData.text,
        type: skillData.type,
        completed: false,
      });
    },
    piniaDeleteSkill(skillId) {
      this.skillSetList = this.skillSetList.filter((object) => object.id !== skillId);
    },
  },
});