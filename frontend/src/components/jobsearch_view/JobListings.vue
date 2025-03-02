<script setup>
import { ref, onMounted } from 'vue';
import jobsearch_api from '../../apis/jobsearch_api';

const jobListings = ref([]);
const headers = ref([
  { title: 'Company', key: 'company' },
  { title: 'Title', key: 'title' },
  { title: 'Experience', key: 'expected_experience' },
  { title: 'Requirement', key: 'requirements' },
  { title: 'Description', key: 'listing' },
  { title: 'Link', key: 'link' },
  { title: 'Date Posted', key: 'date_posted' },
  { title: 'Location', key: 'location' },
  { title: 'Country', key: 'country' },
]);

const selected = ref([]);
const isDialogActive = ref(false);
const activeDescription = ref('');

onMounted(async () => {
  try {
    const response = await jobsearch_api.getJobListings();
    console.log('Fetched job listings:', response.data); // Debugging line
    jobListings.value = response.data.map(item => ({
      ...item,
      truncatedListing: truncateText(item.listing, 20), // Add truncated listing
    }));
  } catch (error) {
    console.error('Error fetching job listings:', error);
  }
});


function truncateText(text, length) {
  if (!text) return 'No description available';
  if (text.length <= length) {
    return text;
  }
  return text.substring(0, length) + '...';
}

function formatDate(dateString) {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

function formatLinkDisplay(url) {
  if (!url) return '';
  // Remove protocol (http:// or https://)
  url = url.replace(/^https?:\/\//i, '');
  // Remove 'www.'
  url = url.replace(/^www\./i, '');
  return url;
}

function ensureProtocol(url) {
  if (!url) return '';
  if (!/^https?:\/\//i.test(url)) {
    return 'https://' + url;
  }
  return url;
}

function openDialog(item) {
  console.log('openDialog func:', item);
  console.log('item:', item.listing);
  activeDescription.value = item.listing || 'No description available';
  isDialogActive.value = true;
}


function closeDialog() {
  isDialogActive.value = false;
}
</script>

<template>
  <v-container class="job-listing-component" fluid>
    <v-row>
      <v-col cols="12">
          <v-data-table
            v-model="selected"
            :items="jobListings"
            :headers="headers"
            item-value="id"
            items-per-page="5"
            show-select
            class="flex-fill"
          >
            <!-- Custom Date Formatting -->
            <template #item.date_posted="{ item }">
              {{ formatDate(item.date_posted) }}
            </template>

            <!-- Custom Template for Description with Dialog -->
            <template #item.listing="{ item }">
              <div>
                <span class="truncated-text" @click="openDialog(item)">
                  {{ truncateText(item.listing, 20) }}
                </span>
              </div>
            </template>

            <!-- Custom Template for Truncated Link -->
            <template #item.link="{ item }">
              <a :href="ensureProtocol(item.link)" target="_blank" rel="noopener noreferrer">
                {{ truncateText(formatLinkDisplay(item.link), 20) }}
              </a>
            </template>
          </v-data-table>
      </v-col>
    </v-row>

    <!-- Dialog Component -->
    <v-dialog v-model="isDialogActive" max-width="800">
      <v-card>
        <v-card-title>
          <span class="text-h6">Job Description</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          {{ activeDescription }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- <pre>{{ selected }}</pre> -->
  </v-container>
</template>

<style scoped>
.truncated-text {
  cursor: pointer;
  text-decoration: underline;
}

.job-listing-component {
  /* display: flex; */
  /* height: 80%; */
}

.v-card-text {
  max-height: 60vh;
  overflow-y: auto;
}

/* Additional styles as needed */
</style>
