<script setup lang="ts">
import {ref, watch} from "vue";

const props = defineProps(['profile'])
const myProfile = ref(props.profile)

watch(() => props.profile, (newValue) => {
  myProfile.value = newValue
})

defineExpose({myProfile})

</script>

<template>
<fieldset class="fieldset">
<label class="label text-base">角色介绍</label>
<textarea class="textarea w-108" v-model="myProfile" rows="6"></textarea>
</fieldset>
</template>

<style scoped>

</style>