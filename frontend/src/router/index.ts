// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  // 你的路由配置
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ 确保有默认导出
export default router