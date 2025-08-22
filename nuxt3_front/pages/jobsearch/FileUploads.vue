<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFileStore } from '~/stores/fileStore';

const selectedFiles = ref([]);
const fileStore = useFileStore();
const loading = ref(false);

// TDD Integration: Metadata controls
const fileType = ref('template');
const language = ref('english');
const jobtype = ref('');
const jobtypes = ref([]);
const industries = ref([]);
const selectedIndustries = ref([]);

// Template-specific fields
const templateSubtype = ref('cover_letter');
const companySize = ref('any');

// CV-specific fields  
const experienceYears = ref(null);
const primaryRoles = ref([]);
const isCurrentCv = ref(false);

onMounted(async () => {
  await fileStore.fetchFiles('cover-letters');
  await fileStore.fetchFiles('images');
  
  // Load dropdown data
  await loadJobtypes();
  await loadIndustries();
});

const loadJobtypes = async () => {
  try {
    const { data } = await $fetch('/files/jobtypes', {
      baseURL: process.client ? 'http://localhost:8080' : 'http://api_gateway:8080'
    });
    jobtypes.value = data || [];
    if (jobtypes.value.length > 0) {
      jobtype.value = jobtypes.value[0].name;
    }
  } catch (error) {
    console.error('Failed to load jobtypes:', error);
  }
};

const loadIndustries = async () => {
  try {
    const { data } = await $fetch('/files/industries', {
      baseURL: process.client ? 'http://localhost:8080' : 'http://api_gateway:8080'
    });
    industries.value = data || [];
  } catch (error) {
    console.error('Failed to load industries:', error);
  }
};

const images = computed(() => fileStore.images);

const uploadedFiles = computed(() => fileStore.uploadedFiles);


const uploadFiles = async () => {
  if (selectedFiles.value.length === 0) {
    alert('Please select at least one file to upload.');
    return;
  }

  loading.value = true;
  try {
    // Use enhanced upload with metadata
    await fileStore.uploadFilesWithMetadata(selectedFiles.value, {
      file_type: fileType.value,
      language: language.value,
      jobtype: jobtype.value,
      industry_sectors: selectedIndustries.value,
      template_subtype: templateSubtype.value,
      company_size_target: companySize.value,
      experience_years: experienceYears.value,
      primary_roles: primaryRoles.value,
      is_current_cv: isCurrentCv.value
    });
    
    selectedFiles.value = []; // Clear the selected files after upload
    
    // Reset metadata forms
    resetMetadataForm();
  } catch (error) {
    alert(`Error uploading files: ${error.response?.data?.detail || error.message}`);
  } finally {
    loading.value = false;
  }
};

const resetMetadataForm = () => {
  fileType.value = 'template';
  language.value = 'english';
  selectedIndustries.value = [];
  templateSubtype.value = 'cover_letter';
  companySize.value = 'any';
  experienceYears.value = null;
  primaryRoles.value = [];
  isCurrentCv.value = false;
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
    <!-- File Selection -->
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
        <v-btn :loading="loading" @click="uploadFiles" color="primary">
          Upload Files
          <template v-slot:loader>
            <v-progress-linear indeterminate color="white"></v-progress-linear>
          </template>
        </v-btn>
      </v-col>
    </v-row>

    <!-- TDD Integration: Red Button Metadata Controls -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="pa-4" title="File Metadata">
          <!-- File Type Red Buttons -->
          <v-row class="mb-3">
            <v-col cols="12">
              <label class="text-subtitle-2">File Type:</label>
              <v-btn-toggle v-model="fileType" mandatory class="mt-2">
                <v-btn value="template" color="red" variant="outlined">Template</v-btn>
                <v-btn value="cv" color="red" variant="outlined">CV</v-btn>
                <v-btn value="application" color="red" variant="outlined">Application</v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>

          <!-- Language Red Buttons -->
          <v-row class="mb-3">
            <v-col cols="12">
              <label class="text-subtitle-2">Language:</label>
              <v-btn-toggle v-model="language" mandatory class="mt-2">
                <v-btn value="english" color="red" variant="outlined">English</v-btn>
                <v-btn value="danish" color="red" variant="outlined">Danish</v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>

          <!-- Jobtype Dropdown -->
          <v-row class="mb-3">
            <v-col cols="6">
              <v-select
                v-model="jobtype"
                :items="jobtypes"
                item-title="name"
                item-value="name"
                label="Job Type"
                hint="Select the target job type"
                persistent-hint
              ></v-select>
            </v-col>
          </v-row>

          <!-- Template-specific fields -->
          <template v-if="fileType === 'template'">
            <v-row class="mb-3">
              <v-col cols="6">
                <v-autocomplete
                  v-model="selectedIndustries"
                  :items="industries"
                  item-title="name"
                  item-value="name"
                  label="Industry Sectors"
                  multiple
                  chips
                  hint="Select relevant industries"
                  persistent-hint
                ></v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-select
                  v-model="companySize"
                  :items="[
                    {value: 'startup', title: 'Startup'},
                    {value: 'mid', title: 'Mid-size'},
                    {value: 'enterprise', title: 'Enterprise'},
                    {value: 'any', title: 'Any Size'}
                  ]"
                  item-title="title"
                  item-value="value"
                  label="Target Company Size"
                ></v-select>
              </v-col>
            </v-row>
          </template>

          <!-- CV-specific fields -->
          <template v-if="fileType === 'cv'">
            <v-row class="mb-3">
              <v-col cols="4">
                <v-text-field
                  v-model="experienceYears"
                  type="number"
                  label="Years of Experience"
                  hint="Total professional experience"
                  persistent-hint
                ></v-text-field>
              </v-col>
              <v-col cols="4">
                <v-autocomplete
                  v-model="primaryRoles"
                  :items="['Data Scientist', 'Software Engineer', 'Project Manager', 'Analyst', 'Consultant']"
                  label="Primary Roles"
                  multiple
                  chips
                  hint="Main professional roles"
                  persistent-hint
                ></v-autocomplete>
              </v-col>
              <v-col cols="4">
                <v-checkbox
                  v-model="isCurrentCv"
                  label="Mark as Current CV"
                  hint="Set as primary CV"
                  persistent-hint
                ></v-checkbox>
              </v-col>
            </v-row>
          </template>
        </v-card>
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