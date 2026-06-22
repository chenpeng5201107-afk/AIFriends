// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Homepageindex from "@/view/homepage/Homepageindex.vue";
import Friendindex from "@/view/friend/Friendindex.vue";
import Createindex from "@/view/create/Createindex.vue";
import NotFoundindex from "@/view/error/NotFoundindex.vue";
import Loginindex from "@/view/user/account/Loginindex.vue";
import Registerindex from "@/view/user/account/Registerindex.vue";
import Spaceindex from "@/view/user/space/Spaceindex.vue";
import Profileindex from "@/view/user/profile/Profileindex.vue";
// @ts-ignore
import { useUserStore } from '@/stores/user'
import UpdateCharacter from "@/view/create/character/UpdateCharacter.vue";


const router = createRouter({
  history: createWebHistory(),
  routes:[
    {
      path: '/',
      component: Homepageindex,
      name: 'Homepageindex',
      meta: {
        needlogin: false,
      },
    },
    {
      path: '/404',
      component: NotFoundindex,
      name: 'NotFoundindex',
       meta: {
        needlogin: false,
      },
    },
    {
      path: '/friend',
      component: Friendindex,
      name: 'Friendindex',
       meta: {
        needlogin: true,
      },
    },
    {
      path:'/create',
      component:Createindex,
      name:'Createindex',
       meta: {
        needlogin: true,
      },
    },
    {
      path:'/create/character/update/:character_id/',
      component:UpdateCharacter,
      name:'Updatecharacter',
       meta: {
        needlogin: true,
      },
    },
    {
      path:'/user/account/login',
      component:Loginindex,
      name:'Loginindex',
      meta: {
        needlogin: false,
      },
    },
    {
      path:'/user/account/register',
      component:Registerindex,
      name:'Registerindex',
      meta: {
        needlogin: false,
      },
    },
    {
      path:'/user/space/:user_id',
      component:Spaceindex,
      name:'Spaceindex',
      meta: {
        needlogin: true,
      },
    },
    {
      path:'/user/profile/',
      component:Profileindex,
      name:'Profileindex',
      meta: {
        needlogin: true,
      },
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404',
      meta: {
        needlogin: false,
      },
      name: 'Notindex',
    }
  ],
})

router.beforeEach((to, from, ) => {
  const user = useUserStore()
  if (to.meta.needlogin && !user.isLogin && user.hasPulledUserInfo) {
    return {
      name: 'Loginindex',
    }
  }
  return true
})

// ✅ 确保有默认导出
export default router