<script setup lang="ts">
import Photo from "@/view/user/profile/components/photo.vue";
import Username from "@/view/user/profile/components/username.vue";
import Profile from "@/view/user/profile/components/profile.vue";
// @ts-ignore
import {useUserStore} from "@/stores/user";
import {ref, useTemplateRef} from "vue";
// @ts-ignore
import {base64ToFile} from '@/js/utils/Base64_to_file'
// @ts-ignore
import api from "@/js/http/api";

const user = useUserStore()

const photoRef:any = useTemplateRef('photo-ref')
const usernameRef:any = useTemplateRef('username-ref')
const profileRef:any = useTemplateRef('profile-ref')
const errorMessage = ref('')

async function handleUpdate() {
  const photo = photoRef.value.myPhoto
  const username = usernameRef.value.myUsername.trim()
  const profile = profileRef.value.myProfile.trim()
  errorMessage.value = ''
  if(!username) {
    errorMessage.value = '用户名不能为空'
  } else if(!profile) {
    errorMessage.value = '简介不能为空'
  } else if(!photo) {
    errorMessage.value = '请上传头像'
  }else{
    const formData = new FormData()
    formData.append('username', username)
    formData.append('profile', profile)
    if ( photo!== user.photo) {
      formData.append('photo',base64ToFile( photo, 'photo.png'))
    }
    try {
      const res = await api.post('/api/user/profile/update/', formData)
      const data = res.data
      if (data.result === 'success') {
        console.log('✅ 更新成功!')
        console.log('  - Username:', data.username)
        console.log('  - Profile:', data.profile)
        user.setUserInfo(data)
      } else {
        errorMessage.value = data.result || '更新失败'
      }
    } catch (error: any){
      console.error('❌ 更新异常:', error)
    }
  }
}
</script>

<template>
<div class="flex justify-center">
  <div class="card bg-base-200 shadow-sm w-120 mt-16">
    <div class="card-body ">
      <h3 class="text-lg font-bold my-4">编辑资料</h3>
      <Photo ref="photo-ref" :photo="user.photo" />
      <Username ref="username-ref" :username="user.username"/>
      <Profile ref="profile-ref" :profile="user.profile"/>

      <p v-if="errorMessage" class="text-red-500 text=sm">{{errorMessage}}</p>

      <div class="flex justify-center">
        <button @click="handleUpdate" class="btn btn-neutral w-60 mt-2">更新</button>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>