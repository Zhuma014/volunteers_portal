<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/api'

const router = useRouter()

const form = ref({
  email: '',
  password: '',
  confirmPassword: '',
  first_name: '',
  last_name: '',
})

const message = ref('')
const isSubmitting = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false) 


const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}
const handleRegister = async () => {
  message.value = ''

  if (form.value.password !== form.value.confirmPassword) {
    message.value = 'Пароли не совпадают'
    alert(message.value)
    return
  }

  isSubmitting.value = true
  try {
    const response = await api.post('/auth/register', {
      email: form.value.email,
      password: form.value.password,
      first_name: form.value.first_name,
      last_name: form.value.last_name,
    })

    message.value = 'Регистрация прошла успешно!'
    alert(message.value)
    router.push('/login')
  } catch (error: any) {
    message.value = error.response?.data?.detail || 'Ошибка при регистрации'
    alert(message.value)
    console.error('Ошибка при регистрации:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="register-container">
    <h1>Регистрация</h1>
    <form @submit.prevent="handleRegister" class="register-form">
      <label>Email:</label>
      <input v-model="form.email" type="email" required />

      <label>Имя:</label>
      <input v-model="form.first_name" required />

      <label>Фамилия:</label>
      <input v-model="form.last_name" required />

      <label>Пароль:</label>
      <div class="password-field">
        <input :type="showPassword ? 'text' : 'password'" v-model="form.password" required />
        <svg @click="togglePassword" class="eye-icon" viewBox="0 0 24 24">
          <path
            d="M12 5c-7 0-11 7-11 7s4 7 11 7 11-7 11-7-4-7-11-7zm0 12c-2.76 0-5-2.24-5-5s2.24-5 5-5 
              5 2.24 5 5-2.24 5-5 5zm0-8a3 3 0 100 6 3 3 0 000-6z"
            fill="#6b7280"
          />
        </svg>
      </div>

      <label>Подтвердите пароль:</label>
      <div class="password-field">
        <input
          :type="showConfirmPassword ? 'text' : 'password'"
          v-model="form.confirmPassword"
          required
        />
        <svg @click="toggleConfirmPassword" class="eye-icon" viewBox="0 0 24 24">
          <path
            d="M12 5c-7 0-11 7-11 7s4 7 11 7 11-7 11-7-4-7-11-7zm0 12c-2.76 0-5-2.24-5-5s2.24-5 5-5 
        5 2.24 5 5-2.24 5-5 5zm0-8a3 3 0 100 6 3 3 0 000-6z"
            fill="#6b7280"
          />
        </svg>
      </div>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Регистрация...' : 'Зарегистрироваться' }}
      </button>

      <p v-if="message" class="message">{{ message }}</p>
    </form>

    <p class="has-account">
      Уже есть аккаунт?
      <RouterLink to="/login">Войдите</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 48px auto;
  padding: 32px 28px 24px 28px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(60, 60, 60, 0.06);
}

h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #22223b;
  margin-bottom: 24px;
  text-align: center;
  letter-spacing: 0.5px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.register-form label {
  font-size: 1rem;
  color: #22223b;
  margin-bottom: 4px;
  font-weight: 500;
}

.register-form input {
  padding: 10px 12px;
  font-size: 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 5px;
  background: #f8fafc;
  transition: border 0.2s;
}

.register-form input:focus {
  border: 1.5px solid #2563eb;
  outline: none;
  background: #fff;
}

.register-form button {
  margin-top: 18px;
  padding: 12px 0;
  font-size: 1.08rem;
  background: linear-gradient(90deg, #005a9c 0%, #0078d4 100%);
  color: #fff;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.register-form button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.message {
  color: red;
  margin-top: 12px;
  text-align: center;
  font-size: 1rem;
}

.has-account {
  margin-top: 18px;
  text-align: center;
  font-size: 0.98rem;
  color: #22223b;
}

.has-account a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: text-decoration 0.2s;
}

.has-account a:hover {
  text-decoration: underline;
}
.password-field {
  position: relative;
  display: flex;
  align-items: center;
}

.password-field input {
  flex: 1;
}

.eye-icon {
  width: 24px;
  height: 24px;
  position: absolute;
  right: 10px;
  cursor: pointer;
  fill: #6b7280;
  transition: fill 0.2s;
}

.eye-icon:hover {
  fill: #374151;
}
</style>
