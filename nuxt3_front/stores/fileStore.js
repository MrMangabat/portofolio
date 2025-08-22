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

    async uploadFilesWithMetadata(files, metadata) {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });

      // Add metadata fields
      formData.append('file_type', metadata.file_type);
      formData.append('language', metadata.language);
      if (metadata.jobtype) formData.append('jobtype', metadata.jobtype);
      if (metadata.industry_sectors?.length) formData.append('industry_sectors', JSON.stringify(metadata.industry_sectors));
      if (metadata.template_subtype) formData.append('template_subtype', metadata.template_subtype);
      if (metadata.company_size_target) formData.append('company_size_target', metadata.company_size_target);
      if (metadata.experience_years) formData.append('experience_years', metadata.experience_years);
      if (metadata.primary_roles?.length) formData.append('primary_roles', JSON.stringify(metadata.primary_roles));
      if (metadata.is_current_cv !== undefined) formData.append('is_current_cv', metadata.is_current_cv);

      try {
        const api = useJobSearchApi();
        const response = await api.uploadFilesWithMetadata(formData);
        console.log('Enhanced upload successful:', response);
        
        // Re-fetch files to update display
        await this.fetchFiles('cover-letters');
        await this.fetchFiles('images');
      } catch (error) {
        console.error('Error uploading files with metadata:', error);
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