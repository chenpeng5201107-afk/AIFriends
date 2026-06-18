<script setup lang="ts">
// @ts-ignore
import {useUserStore} from "@/stores/user"
import Spaceindex from "@/view/user/space/Spaceindex.vue";
import SpaceIcon from "@/component/navbar/icons/SpaceIcon.vue";
import ProfileIcon from "@/component/navbar/icons/ProfileIcon.vue";
import LogoutIcon from "@/component/navbar/icons/LogoutIcon.vue";

const user = useUserStore();

// 收起菜单
function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}

</script>

<template>
  <div class="dropdown dropdown-end">
    <div tabindex="0" role="button" class="avatar btn btn-circle w-8 h-6 mr-6">
      <div class="w-8 rounded-full">
        <img :src="user.photo" alt="">
      </div>
    </div>
    <ul tabindex="-1" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-lg">
      <li>
        <RouterLink @click="closeMenu" :to="{name:'Spaceindex',params:{user_id:user.id}}">
          <div class="avatar">
            <div class="w-10 rounded-full">
              <img :src="user.photo" alt="">
            </div>
          </div>
          <span class="text-base font-bold line-clamp-1">{{user.username}}</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name:'Spaceindex',params:{user_id:user.id}}" class="text-sm font-bold py-3">
          <SpaceIcon/>
          个人空间
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name:'Profileindex'}" class="text-sm font-bold py-3">
          <ProfileIcon/>
          编辑资料
        </RouterLink>
      </li>
      <li>
        <a @click="closeMenu" class="text-sm font-bold py-3">
          <LogoutIcon/>
          退出登录
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>

</style>