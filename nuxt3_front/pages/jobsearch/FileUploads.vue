<!-- frontend/src/components/jobsearch_view/FileUploads.vue -->

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFileStore } from '@/stores/fileStore';

const selectedFiles = ref([]);
const fileStore = useFileStore();

onMounted(async () => {
  await fileStore.fetchFiles('cover-letters');
  await fileStore.fetchFiles('images');
});

const images = computed(() => fileStore.images);

const uploadedFiles = computed(() => fileStore.uploadedFiles);


const uploadFiles = async () => {
  if (selectedFiles.value.length === 0) {
    alert('Please select at least one file to upload.');
    return;
  }

  try {
    await fileStore.uploadFiles(selectedFiles.value);
    selectedFiles.value = []; // Clear the selected files after upload
  } catch (error) {
    alert(`Error uploading files: ${error.response?.data?.detail || error.message}`);
  }
};

const deleteFile = async (file) => {
  // Use the actual MinIO name
  const fileExtension = file.file_name.split('.').pop().toLowerCase();

  let bucketType = '';
  if (['pdf', 'txt'].includes(fileExtension)) {
    bucketType = 'cover-letters';
  } else if (['jpg', 'jpeg', 'png'].includes(fileExtension)) {
    bucketType = 'images';
  } else {
    console.warn(`Unsupported file type: ${fileExtension}`);
    return;
  }

  try {
    // pass file.file_name to the store
    await fileStore.deleteFile(file.file_name, bucketType);
  } catch (error) {
    alert('Error deleting file.');
  }
};

</script>

<template>
  <v-container class="file-upload-container">
    <v-row>
      <v-col cols="9">
        <v-file-input
          v-model="selectedFiles"
          label="Upload PDFs, TXT files, or Images"
          accept=".pdf, .txt, .jpg, .jpeg, .png"
          chips
          multiple
          show-size
        ></v-file-input>
      </v-col>

      <v-col cols="3" class="d-flex justify-end">
        <v-btn :loading="loading" @click="uploadFiles">
          Upload Files
          <template v-slot:loader>
            <v-progress-linear indeterminate color="white"></v-progress-linear>
          </template>
        </v-btn>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <!-- Files Table -->
      <v-col cols="6">
        <h3>Files List</h3>
        <v-data-table
          :items="uploadedFiles"
          :headers="[
            { text: 'File Name', value: 'original_file_name' },
            { text: 'Action', value: 'actions', sortable: false },
          ]"
          item-value="selected"
          show-select
          class="elevation-1"
        >
          <template #item.actions="{ item }">
            <v-btn icon @click="deleteFile(item)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>

      <!-- Images Table -->
      <v-col cols="6">
        <h3>Image List</h3>
        <v-data-table
          :items="images"
          :headers="[
            { text: 'File Name', value: 'original_file_name' },
            { text: 'Action', value: 'actions', sortable: false },
          ]"
          item-value="selected"
          show-select
          class="elevation-1"
        >
          <template #item.actions="{ item }">
            <v-btn icon @click="deleteFile(item)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>


  <v-container class="preview-template-container">
    <h3>Preview uploads</h3>
  </v-container>
</template>

<style scoped>


.checkbox-bordered {
  width: 24px;
  height: 24px;
  border: 1px solid #ccc;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

</style>