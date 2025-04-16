import { reactive } from "vue";
import exercises from "../components/personal_trainer/planning/exercises_test_data.json";

export const personalTrainerStore = reactive({
  exercises: exercises
});
