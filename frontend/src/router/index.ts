import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/NavBar.vue'
import AdminNavBar from '@/components/AdminNavBar.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Layout с обычным NavBar
    {
      path: '/',
      component: NavBar,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/AboutView.vue'),
        },
        {
          path: 'report',
          name: 'report-corruption',
          component: () => import('@/views/ReportCorruptionView.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'cases',
          name: 'cases',
          component: () => import('@/views/CaseListView.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'profile',
          name: 'user-profile',
          component: () => import('@/views/UserProfileView.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'my-courses',
          name: 'my-courses',
          component: () => import('@/views/MyCoursesView.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'courses/:tab(invited|in-progress|completed)',
          name: 'courses-tab',
          component: () => import('@/views/MyCoursesView.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'admin/messages',
          name: 'admin-messages',
          component: () => import('@/views/admin/AdminCasesView.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: '/register',
          name: 'register',
          component: () => import('@/views/RegisterView.vue'),
          meta: { requiresUnauth: true },
        },
        {
          path: '/login',
          name: 'login',
          component: () => import('@/views/LoginView.vue'),
          meta: { requiresUnauth: true },
        },
      ],
    },

    // Без layout
    {
      path: '/login-success',
      name: 'login-success',
      component: () => import('@/views/LoginSuccessView.vue'),
      meta: { requiresUnauth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'login' })
  } else if (to.meta.requiresUnauth && userStore.isLoggedIn) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
