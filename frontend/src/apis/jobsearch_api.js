// frontend/src/apis/jobsearch_api.js
import axios from "axios";

// Get dynamic URLs from the global config loaded in main.js
const API_BASE_URL = window.APP_CONFIG?.API_BASE_URL || "http://localhost:8080";
const COVER_LETTER_BASE_URL = window.APP_CONFIG?.COVER_LETTER_SERVICE_URL || "http://localhost:8080/cover-letter";

// Create an Axios instance for general API calls (if needed)
const fastAPI = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json"
  }
});

// Create an Axios instance for cover letter endpoints
const coverLetterAPI = axios.create({
  baseURL: COVER_LETTER_BASE_URL,
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json"
  }
});

export default {
  // -------------------------------
  // Corrections endpoints (words, sentences, skills)
  // These endpoints are part of the cover letter service.
  // -------------------------------
  addWord(wordData) {
    // wordData should be an object like { text: 'example word' }
    return coverLetterAPI.post("/corrections", { ...wordData, type: 'word' });
  },
  getWords() {
    return coverLetterAPI.get("/corrections", { params: { correction_type: 'word' } });
  },
  deleteWord(wordId) {
    return coverLetterAPI.delete(`/corrections/${wordId}`);
  },
  
  addSentence(sentenceData) {
    return coverLetterAPI.post("/corrections", { ...sentenceData, type: 'sentence' });
  },
  getSentences() {
    return coverLetterAPI.get("/corrections", { params: { correction_type: 'sentence' } });
  },
  deleteSentence(sentenceId) {
    return coverLetterAPI.delete(`/corrections/${sentenceId}`);
  },
  
  addSkill(skillData) {
    return coverLetterAPI.post("/corrections", { ...skillData, type: 'skill' });
  },
  getSkills() {
    return coverLetterAPI.get("/corrections", { params: { correction_type: 'skill' } });
  },
  deleteSkill(skillId) {
    return coverLetterAPI.delete(`/corrections/${skillId}`);
  },
  
  // -------------------------------
  // Job Listings endpoint – served by the API gateway directly
  // -------------------------------
  getJobListings() {
    return fastAPI.get("/job_listings");
  },
  
  // -------------------------------
  // File management endpoints – assuming they belong to the cover letter service
  // -------------------------------
  uploadFiles(formData) {
    return coverLetterAPI.post("/upload_files", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });
  },
  deleteFile(fileName, bucketType) {
    return coverLetterAPI.delete(`/delete_files/${bucketType}/${fileName}`);
  },
  getFiles(bucketType) {
    return coverLetterAPI.get(`/files/${bucketType}`);
  },
};
