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


const router = createRouter({
  history: createWebHistory(),
  routes:[
    {
      path: '/',
      component: Homepageindex,
      name: 'Homepageindex',
    },
    {
      path: '/404',
      component: NotFoundindex,
      name: 'NotFoundindex',
    },
    {
      path: '/friend',
      component: Friendindex,
      name: 'Friendindex',
    },
    {
      path:'/create',
      component:Createindex,
      name:'Createindex'
    },
    {
      path:'/user/account/login',
      component:Loginindex,
      name:'Loginindex'
    },
    {
      path:'/user/account/register',
      component:Registerindex,
      name:'Registerindex'
    },
    {
      path:'/user/space/:user_id',
      component:Spaceindex,
      name:'Spaceindex'
    },
    {
      path:'/user/frofile/',
      component:Profileindex,
      name:'Profileindex',
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404',
    }
  ],
})

// ✅ 确保有默认导出
export default router