<template>
  <div class="profile-container">
    <h1>Личный кабинет</h1>

    <div v-if="loading" class="centered-message">
      <span class="loader"></span> Загрузка...
    </div>

    <div v-else class="profile-card">
      <div class="form-row">
        <label> Почта</label>
        <input :value="user.email" readonly />
      </div>

      <div class="form-row">
        <label> Имя</label>
        <input :value="user.first_name" readonly />
      </div>

      <div class="form-row">
        <label> Фамилия</label>
        <input :value="user.last_name" readonly />
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/api'

interface User {
  id: number
  email: string
  first_name: string
  last_name: string
}

const user = ref<User>({
  id: 0,
  email: '',
  first_name: '',
  last_name: '',
})

const originalUser = ref<User | null>(null)
const newPassword = ref('')
const loading = ref(true)
const editMode = ref(false)

const fetchProfile = async () => {
  loading.value = true
  try {
    const response = await api.get('/profile')
    user.value = { ...response.data }
    originalUser.value = { ...response.data }
  } catch (error) {
    console.error('Ошибка при получении профиля:', error)
  } finally {
    loading.value = false
  }
}



onMounted(fetchProfile)
</script>

<style scoped>
.profile-container {
  max-width: 700px;
  margin: 2.5rem auto;
  padding: 2rem 1.5rem;
  background: #fff;
  border-radius: 18px;
  box-shadow:
    0 4px 24px rgba(0, 87, 184, 0.08),
    0 1.5px 8px rgba(60, 60, 60, 0.07);
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #232323;
  margin-bottom: 1.8rem;
  letter-spacing: 0.01em;
}

.profile-card {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

.form-row {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  color: #232323;
  margin-bottom: 0.4rem;
  font-size: 1.05rem;
}

input {
  padding: 0.8rem 1rem;
  border: 1.5px solid #e5eaf2;
  border-radius: 7px;
  font-size: 1.04rem;
  background: #f4f8fb;
  color: #232323;
  outline: none;
  transition: border 0.18s, box-shadow 0.18s;
}

input:focus {
  border-color: #0057b8;
  box-shadow: 0 2px 8px rgba(0, 87, 184, 0.07);
}

.centered-message {
  text-align: center;
  margin: 2rem 0;
  font-size: 1.1rem;
  color: #232323;
}

.loader {
  display: inline-block;
  width: 1.2em;
  height: 1.2em;
  border: 2px solid #0057b8;
  border-radius: 50%;
  border-top: 2px solid transparent;
  animation: spin 1s linear infinite;
  margin-right: 0.7em;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

</style>
