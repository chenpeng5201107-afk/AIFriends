<script setup lang="ts">
import {ref} from "vue";
import {watch} from "vue";

const props = defineProps(['profile'])
const myProfile = ref(props.profile)


watch(()=>props.profile,newVal=>{
  myProfile.value = newVal
})

defineExpose({
  myProfile,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">简介</label>
    <textarea class="textarea w=108" rows="6" v-model="myProfile">
    </textarea>
  </fieldset>
</template>

<style scoped>

</style>