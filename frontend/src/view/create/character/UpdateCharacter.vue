<script setup lang="ts">

import Photo from "@/view/create/character/components/Photo.vue";
import Name from "@/view/create/character/components/Name.vue";
import Profile from "@/view/create/character/components/Profile.vue";
import BackgroundImage from "@/view/create/character/components/BackgroundImage.vue";
import {onMounted, ref, useTemplateRef} from "vue";
// @ts-ignore
import {base64ToFile} from '@/js/utils/Base64_to_file'
// @ts-ignore
import api from '@/js/http/api'
import {useRoute, useRouter} from "vue-router";
// @ts-ignore
import {useUserStore} from "@/stores/user";

const router = useRouter()
const user = useUserStore()
const route = useRoute()
const character_id:any = route.params.character_id
const character:any = ref(null)

onMounted(async ()=>{
  try {
    const res = await api.get(`/api/create/character/get_single/`,{
      params: {
        character_id: character_id
      }
    })
    const data = res.data
    if (data.result === 'success') {
      character.value = data.character
    }
  } catch (err) {
    console.log(err)
  }
})

const photoRef:any = useTemplateRef('photo-ref')
const nameRef: any = useTemplateRef('name-ref')
const profileRef: any = useTemplateRef('profile-ref')
const backgroundImageRef:any = useTemplateRef('background-image-ref')
const errorMessage = ref('')

async function handleUpdate() {
  const photo = await photoRef.value.myPhoto
  const name = await nameRef.value.myName?.trim()
  const profile = await profileRef.value.myProfile?.trim()
  const backgroundImage = await backgroundImageRef.value.myBackgroundImage

  errorMessage.value = ''
  if(!name) {
    errorMessage.value = '请填写角色名称'
  } else if(!profile) {
    errorMessage.value = '请填写角色简介'
  } else if(!photo) {
    errorMessage.value = '请上传角色头像'
  } else if(!backgroundImage) {
    errorMessage.value = '请上传角色背景图片'
  } else {
    const formData = new FormData()
    formData.append('character_id', character_id)
    formData.append('name', name)
    formData.append('profile', profile)

    if (photo !== character.value.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }
    if (backgroundImage !== character.value.background_image) {
      formData.append('background_image', base64ToFile(backgroundImage, 'backgroundImage.png'))
    }

    try {
      const res= await api.post('/api/create/character/update/', formData)
      const data = res.data
      if (data.result === 'success') {
        await router.push({
          name: 'Spaceindex',
          params: {
            user_id:user.id,
          }
        })
      } else {
        errorMessage.value = data.result || '更新角色失败'
      }
    } catch (error) {
      console.log( error)
    }
  }
}

</script>

<template>
<div v-if="character" class="flex justify-center">
  <div class="card w-120 bg-base-200 shadow-sm mt-16">
    <div class="card-body">
      <h3 class="text-lg font-bold my-4">更新角色</h3>
      <Photo ref="photo-ref" :photo="character.photo"/>
      <Name ref="name-ref" :name="character.name"/>
      <Profile ref="profile-ref" :profile="character.profile"/>
      <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image"/>

      <p v-if="errorMessage" class="text-red-500 text-sm">{{errorMessage}}</p>

      <div class="flex justify-center">
        <button @click="handleUpdate" class="btn btn-neutral w-60 mt-2">更新</button>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>