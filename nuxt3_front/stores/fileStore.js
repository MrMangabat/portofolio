// frontend/src/stores/fileStore.js

import { defineStore } from 'pinia';
import { useJobSearchApi } from '~/composables/useJobSearchApi';

export const useFileStore = defineStore('fileStore', {
  state: () => ({
    uploadedFiles: [],
    extractedTexts: [],
    coverLetters: [],
    images: [],

  }),
  actions: {
    async uploadFiles(files) {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });

      try {
        const api = useJobSearchApi();
        const response = await api.uploadFiles(formData);
        this.uploadedFiles = response.data; // This is the list of ExtractedText or FileItem
        // For clarity, you might also re-fetch the list of files from the server
        await this.fetchFiles('cover-letters');
        await this.fetchFiles('images');
      } catch (error) {
        console.error('Error uploading files:', error);
        throw error;
      }
    },

    async deleteFile(fileName, bucketType) {
      try {
        // We changed the route to /delete_files/<bucketType>/<fileName>
        const api = useJobSearchApi();
        await api.deleteFile(fileName, bucketType);
        // After deletion, re-fetch the list of files
        await this.fetchFiles(bucketType);
      } catch (error) {
        console.error('Error deleting file:', error);
        throw error;
      }
    },

    async fetchFiles(bucketType) {
      try {
        const api = useJobSearchApi();
        const { data } = await api.getFiles(bucketType);
        if (bucketType === 'cover-letters') {
          // Instead of saving to coverLetters, populate the "uploadedFiles" array
          this.uploadedFiles = data.value || [];
        } else if (bucketType === 'images') {
          this.images = data.value || [];
        }
      } catch (error) {
        console.error(`Error fetching files from bucket '${bucketType}':`, error);
        throw error;
      }
    },
  },
});