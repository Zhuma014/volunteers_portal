import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useUserStore } from '@/stores/user'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresUnauth: true } // Доступно только для неавторизованных
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresUnauth: true } // Доступно только для неавторизованных
    },
    // Добавленные маршруты для работы с жалобами
      {
      path: '/report',
      name: 'report-corruption',
      component: () => import('../views/ReportCorruptionView.vue'),
      meta: { requiresAuth: true }
    },
    {
    path: '/cases',
    name: 'cases',
    component: () => import('../views/CaseListView.vue'),
    meta: { requiresAuth: true } 

    },
    {
    path: '/profile',
    name: 'user-profile',
    component: () => import('../views/UserProfileView.vue'),
    meta: { requiresAuth: true } 

     },
     
    {
    path: '/admin/messages',
    name: 'AdminMessages',
    component: () => import('../views/admin/AdminCasesView.vue'),
    meta: { requiresAuth: true } 

    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // Для защищенных роутов проверяем авторизацию
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'login' })
  } 
  // Роуты только для неавторизованных
  else if (to.meta.requiresUnauth && userStore.isLoggedIn) {
    next({ name: 'home' })
  } 
  // Разрешаем переход во всех остальных случаях
  else {
    next()
  }
})

export default router