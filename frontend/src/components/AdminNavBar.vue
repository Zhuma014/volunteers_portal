<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

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
  <nav class="navbar" v-if="isAntikorStaff">
    <div class="navbar-left">
      <router-link class="logo" to="/">Admin Panel</router-link>
    </div>

    <ul class="nav-links">
      <li><router-link to="/admin/messages">Все сообщения</router-link></li>
      <li><router-link to="/my-courses">📚 Мои курсы</router-link></li>

      <li class="dropdown">
        <button class="dropbtn">
          👤 Кабинет <span class="arrow">▼</span>
        </button>
        <div class="dropdown-content">
          <RouterLink to="/profile">Профиль</RouterLink>
          <RouterLink to="/admin/users">Все пользователи</RouterLink>
          <button @click="openCanvasLogoutThenLogout">Выйти</button>
        </div>
      </li>
    </ul>
  </nav>
</template>



<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.navbar {
  font-family: 'Inter', sans-serif;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 80px;
  padding: 0 2rem;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo {
  font-size: 1.4rem;
  font-weight: 600;
  color: #111827;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-links a {
  color: #374151;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.nav-links a:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.dropdown {
  position: relative;
}

.dropbtn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: none;
  border: none;
  color: #374151;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.dropbtn:hover {
  background-color: #f3f4f6;
}

.arrow {
  font-size: 0.75rem;
  opacity: 0.6;
}

.dropdown-content {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  flex-direction: column;
  min-width: 180px;
  z-index: 999;
  animation: fadeIn 0.2s ease-in-out;
}

.dropdown-content a,
.dropdown-content button {
  padding: 0.75rem 1rem;
  color: #374151;
  font-size: 0.95rem;
  background: none;
  border: none;
  text-align: left;
  width: 100%;
  cursor: pointer;
  transition: background 0.2s ease;
}

.dropdown-content a:hover,
.dropdown-content button:hover {
  background-color: #f9fafb;
  color: #111827;
}

.dropdown:hover .dropdown-content {
  display: flex;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
