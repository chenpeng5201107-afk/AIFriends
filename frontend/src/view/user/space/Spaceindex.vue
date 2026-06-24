<script setup lang="ts">
import UserInfoField   from "@/view/user/space/components/UserInfoField.vue";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef} from "vue";
// @ts-ignore
import api from '@/js/http/api'
import {useRoute} from "vue-router";

const userProfile: any = ref(null)
const characters: any = ref([])
let isLoading: any = ref(false)
const hasCharacters: any = ref(true)
const sentinelRef: any = useTemplateRef('sentinel')
const route = useRoute()

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}


async function loadMore() {
  if (isLoading.value || !hasCharacters.value) return

  isLoading.value = true
  let newCharacters: any[] = []

  try {
    console.log('🔍 开始请求，user_id:', route.params.user_id)
    console.log('🔍 当前 characters 数量:', characters.value.length)

    const res = await api.get('/api/create/character/get_list/', {
      params: {
        items_count: characters.value.length,
        user_id: route.params.user_id
      }
    })

    console.log('✅ API 返回:', res)
    console.log('✅ data:', res.data)
    console.log('✅ result:', res.data.result)

    const data = res.data
    if (data.result === 'success') {
      console.log('✅ user_profile:', data.user_profile)
      userProfile.value = data.user_profile
      newCharacters = data.characters
    } else {
      console.error('❌ API 返回失败:', data.result)
    }
  } catch (err) {
    console.error('❌ 请求失败:', err)
  } finally {
    isLoading.value = false

    if (newCharacters.length === 0) {
      hasCharacters.value = false
    } else {
      characters.value.push(...newCharacters)
      await nextTick()

      if (checkSentinelVisible() && !isLoading.value && hasCharacters.value) {
        await loadMore()
      }
    }
  }
}

let observer: any = null
onMounted(async () => {
  await loadMore()

  observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        loadMore()
      }
    })
  },{
    root: null,rootMargin: '2px',threshold: 0
  })
  observer.observe(sentinelRef.value)
})

onBeforeUnmount(()=>{
  observer?.disconnect()
})
</script>

<template>
 <div class="flex flex-col items-center mb-12">
     <UserInfoField :userProfile="userProfile"/>
     <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
      </div>
   <div ref="sentinel" class="h-2 w-100 mt-8 bg-red-500"></div>
   <div v-if="isLoading" class="text-gray-500 mt-4">加载中...</div>
   <div v-else-if="!hasCharacters" class="text-gray-500 mt-4">没有更多角色了</div>

 </div>
</template>

<style scoped>

</style>