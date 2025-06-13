<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/api' // 

const router = useRouter()

const form = ref({
  iin: '',
  phone_number: '',
  password: '',
  first_name: '',
  last_name: '',
})

const handleRegister = async () => {
  try {
    const response = await api.post('/auth/register', form.value)

    alert('Регистрация прошла успешно!')
    router.push('/login')
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Ошибка при регистрации'
    alert(message)
    console.error('Ошибка при регистрации:', error)
  }
}
</script>

<template>
  <div class="register-container">
    <h1>Регистрация</h1>
    <form @submit.prevent="handleRegister" class="register-form">
      <label>ИИН:</label>
      <input v-model="form.iin" required />

      <label>Номер телефона:</label>
      <input v-model="form.phone_number" />

      <label>Имя:</label>
      <input v-model="form.first_name" required />

      <label>Фамилия:</label>
      <input v-model="form.last_name" required />

      <label>Пароль:</label>
      <input type="password" v-model="form.password" required />

      <button type="submit">Зарегистрироваться</button>
    </form>

    <p class="has-account">
      Уже есть аккаунт?
      <RouterLink to="/login">Войдите</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.register-form label {
  margin-top: 1rem;
}

.register-form input {
  padding: 0.5rem;
  font-size: 1rem;
}

.register-form button {
  margin-top: 2rem;
  padding: 0.75rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.has-account {
  margin-top: 1rem;
  text-align: center;
}

.has-account a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}
</style>
