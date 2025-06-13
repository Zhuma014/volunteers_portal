<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api/api'

const router = useRouter()
const authStore = useUserStore()

const form = ref({
  iin: '',
  password: '',
})

const handleLogin = async () => {
  try {
    const response = await api.post('/auth/login', form.value)

    const data = response.data
    authStore.login(data.access_token)
    router.push('/')
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Ошибка при входе'
    alert(message)
    console.error(error)
  }
}
</script>


<template>
  <div class="login-container">
    <h1>Вход в систему</h1>
    <form @submit.prevent="handleLogin" class="login-form">
      <label>ИИН:</label>
      <input v-model="form.iin" required />

      <label>Пароль:</label>
      <input type="password" v-model="form.password" required />

      <button type="submit">Войти</button>
    </form>

    <p class="no-account">
      Нет аккаунта?
      <RouterLink to="/register">Зарегистрируйтесь</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.login-form label {
  margin-top: 1rem;
}

.login-form input {
  padding: 0.5rem;
  font-size: 1rem;
}

.login-form button {
  margin-top: 2rem;
  padding: 0.75rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.no-account {
  margin-top: 1rem;
  text-align: center;
}

.no-account a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}
</style>
