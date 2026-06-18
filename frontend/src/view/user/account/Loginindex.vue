<script setup lang="ts">
// @ts-ignore
import {useUserStore} from "@/stores/user";
// @ts-ignore
import api from '@/js/http/api'
import {ref} from "vue";
import {useRouter} from "vue-router";

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const user = useUserStore()
const router = useRouter()

async function handleLogin(){
  errorMessage.value = ''
  isLoading.value = true

  if (!username.value || !password.value) {
    errorMessage.value = '请填写用户名和密码'
    isLoading.value = false
    return
  }

  try {
    console.log('📤 发送登录请求:', {
      username: username.value,
      password: '***'
    })

    const res = await api.post('/api/user/account/login/', {
      username: username.value.trim(),
      password: password.value.trim(),
    })

    // 🔍 关键调试信息
    console.log('📥 收到响应:')
    console.log('  - 状态码:', res.status)
    console.log('  - 响应数据:', res.data)
    console.log('  - 数据大小:', JSON.stringify(res.data).length, '字节')
    console.log('  - 所有字段:', Object.keys(res.data))

    const data = res.data

    // 检查是否有 result 字段
    if (!data.result) {
      console.error('❌ 响应中没有 result 字段!')
      errorMessage.value = '服务器响应格式错误'
      isLoading.value = false
      return
    }

    if(data.result === '登录成功~') {
      console.log('✅ 登录成功!')

      // 检查 token 字段
      const token = data.access || data.token
      console.log('  - Token 字段:', token ? '存在' : '不存在')
      console.log('  - Token 值:', token ? token.substring(0, 20) + '...' : '无')

      if (!token) {
        console.error('❌ 没有找到 token 字段!')
        errorMessage.value = '登录失败：未获取到令牌'
        isLoading.value = false
        return
      }

      // 存储用户信息
      user.setAccessToken(token)
      user.setUserInfo(data)

      console.log('📦 用户信息已存储')
      console.log('  - User ID:', data.user_id)
      console.log('  - Username:', data.username)

      // 跳转
      console.log('🚀 准备跳转到首页')
      await router.push({ name: 'Homepageindex' })
      console.log('✅ 跳转完成')

    } else {
      console.log('❌ 登录失败:', data.result)
      errorMessage.value = data.result || '登录失败'
    }

  } catch (error: any) {
    console.error('❌ 请求异常:', error)

    if (error.response) {
      console.error('  - 状态码:', error.response.status)
      console.error('  - 错误数据:', error.response.data)
      errorMessage.value = error.response.data?.result || `请求失败 (${error.response.status})`
    } else if (error.request) {
      console.error('  - 无响应:', error.request)
      errorMessage.value = '服务器无响应，请检查网络'
    } else {
      console.error('  - 配置错误:', error.message)
      errorMessage.value = '请求配置错误'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex justify-center mt-30">
    <form @submit.prevent="handleLogin" class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
      <label class="label">用户名</label>
      <input v-model="username" type="text" class="input" placeholder="用户名" />

      <label class="label">密码</label>
      <input v-model="password" type="password" class="input" placeholder="密码" />

      <p class="text-sm text-red-500 mt-1" v-if="errorMessage">{{ errorMessage }}</p>

      <button class="btn btn-neutral mt-4" :disabled="isLoading">
        {{ isLoading ? '登录中...' : '登录' }}
      </button>

      <div class="flex justify-end">
        <RouterLink :to="{name: 'Registerindex'}" class="btn btn-sm btn-ghost text-gray-500">
          注册
        </RouterLink>
      </div>
    </form>
  </div>
</template>