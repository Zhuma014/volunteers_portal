<template>
  <div class="container">
    <h1>Личный кабинет</h1>

    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <label>ИИН:</label>
      <input :value="user.iin" readonly />

      <label>Имя:</label>
      <input :value="user.first_name" readonly />

      <label>Фамилия:</label>
      <input :value="user.last_name" readonly />

      <label>Роль:</label>
      <input :value="roleTranslations[user.role]" readonly />

      <label>Активен:</label>
      <input :value="user.is_active ? 'Да' : 'Нет'" readonly />

      <label>Дата регистрации:</label>
      <input :value="formatDate(user.created_at)" readonly />

      <label>Номер телефона:</label>
      <input v-model="user.phone_number" :readonly="!editMode" />

      <div class="actions">
        <button v-if="!editMode" @click="editMode = true">Редактировать</button>
        <div v-else>
          <button @click="saveProfile" style="margin-right: 1rem;">Сохранить</button>

          <button @click="cancelEdit">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import { roleTranslations } from '@/constants/roleTranslations'


interface User {
  id: number
  iin: string
  phone_number: string | null
  role: string
  is_active: boolean
  created_at: string
  first_name: string
  last_name: string
}

const user = ref<User>({
  id: 0,
  iin: '',
  phone_number: '',
  role: '',
  is_active: false,
  created_at: '',
  first_name: '',
  last_name: '',
})

const originalUser = ref<User | null>(null)
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

const saveProfile = async () => {
  try {
    await api.put('/profile', {
      phone_number: user.value.phone_number,
    })
    editMode.value = false
    await fetchProfile()
  } catch (error) {
    alert('Ошибка при сохранении')
  }
}

const cancelEdit = () => {
  if (originalUser.value) {
    user.value.phone_number = originalUser.value.phone_number
  }
  editMode.value = false
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

onMounted(fetchProfile)
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 1rem;
  font-weight: bold;
}

input {
  padding: 0.5rem;
  margin-top: 0.3rem;
  margin-bottom: 0.7rem;
  width: 100%;
  box-sizing: border-box;
}

.actions {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
}

button {
  padding: 0.6rem 1.2rem;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
</style>
