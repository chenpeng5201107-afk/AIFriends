<script setup lang="ts">
import NavBar from "@/component/navbar/NavBar.vue";
import {onMounted} from "vue";
// @ts-ignore
import api from "@/js/http/api";
// @ts-ignore
import {useUserStore} from "@/stores/user";
import {useRoute, useRouter} from "vue-router";

const user = useUserStore()
const router = useRouter()
const route = useRoute()

onMounted(async () => {
  try {
    const res = await api.get('/api/user/account/get_user_info/')
    const data = res.data
    if (data.result === 'success') {
      user.setUserInfo(data)
    }
  } catch (err) {
    console.log(err)
  } finally {
    user.setHasPulledUserInfo(true)

    if(route.meta.needlogin && !user.isLogin()) {
      await router.replace( {
        name: 'Loginindex',
      })
    }
  }
})
</script>

<template>
<NavBar>
  <RouterView/>
</NavBar>
</template>

<style scoped>

</style>
