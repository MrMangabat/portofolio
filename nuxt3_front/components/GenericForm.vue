<template>
  <div>
    <form @submit.prevent="handleSubmit">
      <v-row class="mt-3">
        <v-col cols="12">
          <v-text-field
            v-model="model[props.inputProperty]"
            :label="props.label"
            type="text"
            class="centered-label"
            style="width:100%; margin-bottom:-30px;"
          />
        </v-col>
      </v-row>

      <v-row class="mb-3">
        <v-col cols="12" class="d-flex justify-center">
          <v-btn type="submit" color="primary">Add</v-btn>
        </v-col>
      </v-row>
    </form>
  </div>
</template>

<script setup>
import { reactive, toRefs } from 'vue'

const props = defineProps({
  apiAddFn: Function,
  piniaAddFn: Function,
  inputProperty: String,
  label: String,
  validationErrorMessage: String
})

const model = reactive({ [props.inputProperty]: '' })

function handleSubmit() {
  const val = model[props.inputProperty]
  if (typeof val !== 'string' || !val.trim()) {
    alert(props.validationErrorMessage)
    return
  }
  props.apiAddFn(val)
    .then(() => {
      props.piniaAddFn(val)
      model[props.inputProperty] = ''
    })
    .catch(err => console.error(err))
}
</script>

<style scoped>
.centered-label ::v-deep .v-field-label {
  text-align: center;
  width: 100%;
}
.mt-3 { margin-top: 12px; }
.mb-3 { margin-bottom: 12px; }
</style>
