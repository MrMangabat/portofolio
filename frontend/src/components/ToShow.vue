<script setup>

defineProps({
  work_experiences: {
    type: Object,
    required: true
  },
})
</script>

<template>
  <div class="to-show">
    <!-- Display introduction-->
    <h1>{{ work_experiences.company_name }}</h1>
    <h2>{{ work_experiences.job_title }}</h2>
    <h4>{{ work_experiences.start_date}}</h4>
    <h4>{{ work_experiences.end_date}}</h4>
    <p>{{ work_experiences.job_description }}</p>
  </div>

</template>

<style scoped>
.to-show {
  padding: 20px;
  width: 250px;
  cursor: pointer;
  border: 1px solid #39495c;
  margin-bottom: 18px;
}
.to-show:hover {
  transform: scale(1.01);
  box-shadow: 0 3px 12px 0 rgba(0, 0, 0, 0.2);
}
</style>
