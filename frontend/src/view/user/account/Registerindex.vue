<script setup lang="ts">

// @ts-ignore
import {useUserStore} from "@/stores/user";
// @ts-ignore
import api from '@/js/http/api'
import {ref} from "vue";
import {useRouter} from "vue-router";
const user = useUserStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const password2 = ref('')

async function handeleRegister() {
  errorMessage.value = ''
  if (!username.value) {
    errorMessage.value = '用户名不能为空'
  } else if (!password.value) {
    errorMessage.value = '密码不能为空'
  } else if (password.value !== password2.value) {
    errorMessage.value = '密码不一致'
  } else {
    try {
      const res = await api.post('/api/user/account/register/', {
        username: username.value.trim(),
        password: password.value.trim(),
      })
      const data = res.data
      if (data.result === '注册成功~') {
        console.log('✅ 注册成功!')
        console.log('  - User ID:', data.user_id)
        console.log('  - Username:', data.username)
        console.log('  - Token 字段:', data.access ? '存在' : '不存在')
        console.log('  - Token 值:', data.access ? data.access.substring(0, 20) + '...' : '无')
        console.log('  - 跳转中...')
        user.setAccessToken(data.access)
        user.setUserInfo(data)
        await router.push({name: 'Homepageindex'})
      } else {
        errorMessage.value = data.result || '注册失败'
      }
    } catch (error: any) {
      console.error('❌ 登录异常:', error)
    }
  }
}

</script>

<template>
  <div class="flex justify-center mt-30">
      <form @submit.prevent="handeleRegister" class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">

      <label class="label">用户名</label>
      <input v-model='username' type="text" class="input" placeholder="用户名" />

      <label class="label">密码</label>
      <input v-model='password' type="password" class="input" placeholder="密码" />

      <label class="label">确认密码</label>
      <input v-model='password2' type="password" class="input" placeholder="确认密码" />

      <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{errorMessage}}</p>

      <button class="btn btn-neutral mt-4">注册</button>
      <div class="flex justify-end">
        <RouterLink :to="{name: 'Loginindex'}" class="btn btn-sm btn-ghost text-gray-500">
         登录
        </RouterLink>
      </div>
  </form>
  </div>
</template>

<style scoped>

</style>