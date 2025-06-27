<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import logo from '@/assets/logo/_gluster_2020_1_5_d7a1c76e17ab08a7ace0b1bc60c50691_1280x720-removebg-preview (1).png'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const user = computed(() => userStore.user)
const isAntikorStaff = computed(() => user.value?.role === 'antikor_staff')

const router = useRouter()

const openCanvasLogoutThenLogout = () => {
  const canvasLogoutUrl = 'http://172.23.148.229/logout'
  const popup = window.open(canvasLogoutUrl, '_blank')
  if (!popup) {
    alert('Браузер заблокировал всплывающее окно. Разрешите их для выхода из Canvas.')
  }
  userStore.logout()
  localStorage.clear()
}
</script>

<template>
  <div class="portal-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <router-link class="sidebar-logo" to="/">
          <img :src="logo" alt="Logo" />
        </router-link>
      </div>

      <ul class="sidebar-links">
        <!-- Admin Sidebar -->
        <template v-if="isAntikorStaff">
          <li>
            <router-link to="/admin/messages"
              ><span class="icon">📩</span>Все сообщения</router-link
            >
          </li>
          <li>
            <router-link to="/my-courses"><span class="icon">📚</span>Курсы</router-link>
          </li>
          <li class="sidebar-dropdown">
            <button class="sidebar-dropbtn">
              <span class="icon">👤</span>Кабинет<span class="arrow">▼</span>
            </button>
            <div class="sidebar-dropdown-content">
              <router-link to="/profile">Профиль</router-link>
              <button @click="openCanvasLogoutThenLogout">Выйти</button>
            </div>
          </li>
        </template>

        <!-- Logged-in User Sidebar -->
        <template v-else-if="isLoggedIn">
          <li>
            <router-link to="/"><span class="icon">🏠</span>Главная</router-link>
          </li>
          <li>
            <router-link to="/report"><span class="icon">📝</span>Сообщить о коррупции</router-link>
          </li>
          <li>
            <router-link to="/my-courses"><span class="icon">📚</span>Курсы</router-link>
          </li>
          <li>
            <router-link to="/about"><span class="icon">ℹ️</span>О нас</router-link>
          </li>
          <li class="sidebar-dropdown">
            <button class="sidebar-dropbtn">
              <span class="icon">👤</span>Кабинет<span class="arrow">▼</span>
            </button>
            <div class="sidebar-dropdown-content">
              <router-link to="/profile">Профиль</router-link>
              <router-link to="/cases">Мои сообщения</router-link>
              <button @click="openCanvasLogoutThenLogout">Выйти</button>
            </div>
          </li>
        </template>

        <!-- Guest Sidebar -->
        <template v-else>
          <li>
            <router-link to="/"><span class="icon">🏠</span>Главная</router-link>
          </li>
          <li>
            <router-link to="/about"><span class="icon">ℹ️</span>О нас</router-link>
          </li>
          <li>
            <router-link to="/login"><span class="icon">👤</span>Войти</router-link>
          </li>
        </template>
      </ul>
    </aside>

    <main class="portal-main">
      
      
      <section class="portal-content">
        <router-view />
      </section>
    </main>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.portal-layout {
  display: flex;
  height: 100vh;
  font-family: 'Inter', sans-serif;
  background: #f9fafb;
}

/* Сайдбар */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 240px;
  height: 100vh;
  background-color: #ffffff;
  color: #1f2937;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e5e7eb;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.05);
  z-index: 1000;
}

/* Логотип */
.sidebar-header {
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px; /* такой же, как .portal-header */
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.sidebar-logo img {
  height: 130px; /* точно как .portal-header */
  width: auto;
  object-fit: contain;
}

/* Навигация */
.sidebar-links {
  flex-grow: 1;
  list-style: none;
  padding: 0.75rem 0;
  margin: 0;
}
.sidebar-links li {
  width: 100%;
}
.sidebar-links a,
.sidebar-dropbtn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: #374151;
  text-decoration: none;
  font-size: 0.96rem;
  font-weight: 500;
  border-radius: 8px;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease;
}
.sidebar-links a:hover,
.sidebar-dropbtn:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.icon {
  font-size: 1.1rem;
}

/* Дропдаун */
.sidebar-dropdown {
  position: relative;
}
.sidebar-dropbtn .arrow {
  margin-left: auto;
  font-size: 0.75rem;
  opacity: 0.5;
}
.sidebar-dropdown-content {
  position: absolute;
  left: 10%;
  top: 100%;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  display: none;
  flex-direction: column;
  width: 80%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  z-index: 999;
}

.sidebar-dropdown-content a,
.sidebar-dropdown-content button {
  padding: 0.75rem 1rem;
  color: #374151;
  font-size: 0.95rem;
  background: none;
  border: none;
  text-align: left;
  width: 100%;
  cursor: pointer;
}
.sidebar-dropdown-content a:hover,
.sidebar-dropdown-content button:hover {
  background-color: #f9fafb;
  color: #111827;
}
.sidebar-dropdown:hover .sidebar-dropdown-content {
  display: flex;
}

.login-btn {
  font-weight: 600;
}

/* Контент */
.portal-main {
  margin-left: 240px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.portal-header {
  height: 80px;
  padding: 0.4rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
}
.portal-header h1 {
  font-size: 1.75rem;
  margin: 0;
  color: #111827;
}

.portal-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>
