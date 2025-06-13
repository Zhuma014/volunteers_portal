<template>
  <AdminNavBar v-if="userStore.isAdmin" />
  <NavBar v-else />
  <RouterView />
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/NavBar.vue'
import AdminNavBar from '@/components/AdminNavBar.vue'

const userStore = useUserStore()
</script>

<style scoped>
header {
  background-color: #f8f9fa;
  padding: 1rem;
  border-bottom: 1px solid #ccc;
}

nav {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

nav a {
  text-decoration: none;
  color: #333;
}

nav a.router-link-exact-active {
  font-weight: bold;
  color: #007bff;
}
</style>
