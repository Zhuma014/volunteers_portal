<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)

const router = useRouter()

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <div class="navbar-left">
      <router-link class="logo" to="/">Adal Volunteers</router-link>
    </div>

    <ul class="nav-links">
      <li><router-link to="/">Главная</router-link></li>

      <li><router-link to="/report">Сообщить о коррупции</router-link></li>

      <li><router-link to="/about">О нас</router-link></li>

      <li v-if="isLoggedIn" class="dropdown">
        <button class="dropbtn">
          👤 Кабинет
          <span class="arrow">▼</span>
        </button>
        <div class="dropdown-content">
          <RouterLink to="/profile">Профиль</RouterLink>
          <RouterLink to="/cases">Мои сообщения</RouterLink>
          <button @click="handleLogout">Выйти</button>
        </div>
      </li>

      <li v-else>
        <router-link class="login-btn" to="/login">Войти</router-link>
      </li>
    </ul>
  </nav>
</template>


<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: linear-gradient(90deg, #2c3e50, #4ca1af);
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  list-style: none;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.nav-links a:hover {
  background-color: rgba(255, 255, 255, 0.15);
}



.dropdown {
  position: relative;
}

.dropbtn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font: inherit;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.arrow {
  font-size: 0.75rem;
}

.dropdown-content {
  display: none;
  position: absolute;
  right: 0;
  top: 110%;
  background-color: white;
  color: black;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  overflow: hidden;
  min-width: 160px;
  z-index: 10;
  flex-direction: column;
  animation: fadeIn 0.2s ease-in-out;
}

.dropdown-content a,
.dropdown-content button {
  padding: 0.75rem 1rem;
  text-align: left;
  text-decoration: none;
  border: none;
  background: none;
  color: black;
  cursor: pointer;
  width: 100%;
  transition: background 0.2s ease;
}

.dropdown-content a:hover,
.dropdown-content button:hover {
  background-color: #f3f4f6;
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
