<script setup lang="ts">
import {ref} from "vue";
// @ts-ignore
import {useUserStore} from "@/stores/user";
import Update from "@/component/character/icons/Update.vue";
import Remove from "@/component/character/icons/Remove.vue";

const props = defineProps(['character', 'canEdit'])
const isHover = ref(false)
const user = useUserStore()

</script>

<template>
<div>
  <div class="avatar cursor-pointer" @mouseover="isHover=true" @mouseout="isHover=false">
    <div class="w-60 h-100 rounded-2xl relative">
      <img :src="character.background_image" class="transition-transform duration-300" :class="{'scale-120':isHover}" alt="">
      <div class="absolute left-0 top-50 w-60 h-50 bg-linear-to-t from-black/40 to-transparent"></div>

      <div v-if="canEdit && character.author.user_id === user.id" class="absolute left=0 top-50">
        <RouterLink :to="{
          name:'Updatecharacter',
          params:{
            character_id:character.id
          }
        }" class="btn btn-circle btn-ghost bg-transparent">
          <Update/>
        </RouterLink>
        <button class="btn btn-circle btn-ghost bg-transparent">
          <Remove/>
        </button>
      </div>

      <div class="absolute left-4 top-54 avatar">
        <div class="w-16 rounded-full ring-3 ring-white">
          <img :src="character.photo" alt="">
        </div>
      </div>
      <div class="absolute">

      </div>
    </div>

  </div>
  <div>

  </div>
</div>
</template>

<style scoped>

</style>