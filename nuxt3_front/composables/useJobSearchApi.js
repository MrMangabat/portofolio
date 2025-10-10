// composables/useJobSearchApi.js
export const useJobSearchApi = () => {

  const config = useRuntimeConfig();
  const API_BASE_URL = process.client 
  ? config.public.apiBaseUrl    // Browser: localhost:8080
  : config.apiBaseUrl          // SSR: api_gateway:8080

  console.log('🔧 API_BASE_URL:', API_BASE_URL);
  return {
    // ===== GET REQUESTS - Use useFetch (SSR-safe) =====
    async getSkills() {
      return await useFetch('/corrections', {
        baseURL: API_BASE_URL,
        query: { correction_type: 'skill' },
        key: 'skills',
      })
    },
    
    async getWords() {
      return await useFetch('/corrections', {
        baseURL: API_BASE_URL,
        query: { correction_type: 'word' },
        key: 'words',
      })
    },
    
    async getSentences() {
      return await useFetch('/corrections', {
        baseURL: API_BASE_URL,
        query: { correction_type: 'sentence' },
        key: 'sentences',
      })
    },

    async getJobListings() {
      return await useFetch('/job_listings', {
        baseURL: API_BASE_URL,
        key: 'job-listings',
      })
    },

    async getFiles(bucketType) {
      return await useFetch(`/files/${bucketType}`, {
        baseURL: API_BASE_URL,
        key: `files-${bucketType}`,
      })
    },

    // ===== POST/PUT/DELETE REQUESTS - Use $fetch (client-only operations) =====
    async addSkill(skillData) {
      const response = await $fetch('/corrections', {
        method: 'POST',
        baseURL: API_BASE_URL,
        body: { ...skillData, type: 'skill' }
      })
      return { data: response }
    },
    
    async deleteSkill(skillId) {
      return await $fetch(`/corrections/${skillId}`, {
        method: 'DELETE',
        baseURL: API_BASE_URL
      })
    },

    async addWord(wordData) {
      const response = await $fetch('/corrections', {
        method: 'POST',
        baseURL: API_BASE_URL,
        body: { ...wordData, type: 'word' }
      })
      return { data: response }
    },
    
    async deleteWord(wordId) {
      return await $fetch(`/corrections/${wordId}`, {
        method: 'DELETE',
        baseURL: API_BASE_URL
      })
    },

    async addSentence(sentenceData) {
      const response = await $fetch('/corrections', {
        method: 'POST',
        baseURL: API_BASE_URL,
        body: { ...sentenceData, type: 'sentence' }
      })
      return { data: response }
    },
    
    async deleteSentence(sentenceId) {
      return await $fetch(`/corrections/${sentenceId}`, {
        method: 'DELETE',
        baseURL: API_BASE_URL
      })
    },

    // ===== FILE MANAGEMENT =====
    async uploadFiles(formData) {
      return await $fetch('/files/upload', {
        method: 'POST',
        baseURL: API_BASE_URL,
        body: formData
      })
    },
    
    async deleteFile(fileName, bucketType) {
      return await $fetch(`/files/${bucketType}/${fileName}`, {
        method: 'DELETE',
        baseURL: API_BASE_URL
      })
    },
    
    // Enhanced upload with metadata
    async uploadFilesWithMetadata(formData) {
      return await $fetch('/files/upload-with-metadata', {
        method: 'POST',
        baseURL: API_BASE_URL,
        body: formData
      })
    }
  }
}