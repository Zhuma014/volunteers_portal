<template>
  <div class="container">
    <h1>Мои жалобы</h1>

    <div v-if="loading">Загрузка...</div>
    <div v-else-if="cases.length === 0">У вас нет жалоб</div>

    <table class="case-table" v-else>
      <thead>
        <div style="margin: 1rem 0;">
  <label for="status-filter">Фильтровать по статусу:</label>
  <select id="status-filter" v-model="selectedStatus">
    <option value="">Все</option>
    <option v-for="(label, key) in statusTranslations" :key="key" :value="key">
      {{ label }}
    </option>
  </select>
</div>
        <tr>
          <th>Заголовок</th>
          <th>Адрес</th>
          <th>Статус</th>
          <th>Действия</th>
          
        </tr>
        
      </thead>
      
      <tbody>
<tr v-for="item in filteredCases" :key="item.id">
  <td>{{ item.title }}</td>
  <td>{{ item.address }}</td>
  <td>{{ statusTranslations[item.status] || item.status }}</td>
  <td>
        <div style="display: flex; gap: 8px;">

    <button @click="openViewModal(item.id)">Посмотреть</button>
    
    <!-- Показывать "Изменить" и "Удалить" только если статус не in_review, accepted или rejected -->
    <template v-if="!['in_review', 'accepted', 'rejected'].includes(item.status)">
      <button @click="openEditModal(item.id)">Изменить</button>
      <button @click="deleteCase(item.id)">Удалить</button>
    </template>
    </div>
  </td>
</tr>

        
      </tbody>
    </table>

    <!-- Модальное окно -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2 v-if="editMode">Редактировать жалобу</h2>
        <h2 v-else>Просмотр жалобы</h2>

        <div class="modal-content">
          <label>Заголовок:</label>
          <input v-model="selectedCase.title" :readonly="!editMode" />

          <label>Описание:</label>
          <textarea v-model="selectedCase.description" :readonly="!editMode"></textarea>

          <label>Адрес:</label>
          <input v-model="selectedCase.address" :readonly="!editMode" />

<div v-if="!editMode">
    <p>
    <strong>
      {{
        selectedCase.status === 'accepted'
          ? '✅ Одобрено'
          : selectedCase.status === 'rejected'
          ? '❌ Отказано'
          : '⏳ В ожидании'
      }}
    </strong>
  </p>
</div>
<div v-if="!editMode && selectedCase.feedbacks && selectedCase.feedbacks.length > 0">
  <ul>
    <li v-for="fb in selectedCase.feedbacks" :key="fb.id">
      <strong>📩 Отзыв:</strong> {{ fb.message }}
    </li>
  </ul>
</div>



          <div class="modal-actions">
            <button @click="closeModal">Закрыть</button>
            <button v-if="editMode" @click="saveCase">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/api/api'
import { statusTranslations } from '@/constants/statusTranslations'



interface Case {
  id: number
  title: string
  description: string
  address: string
  status: string
}
const selectedStatus = ref('')

const filteredCases = computed(() => {
  if (!selectedStatus.value) return cases.value
  return cases.value.filter(c => c.status === selectedStatus.value)
})
const cases = ref<Case[]>([])
const loading = ref(true)

const showModal = ref(false)
const selectedCase = ref<Case | null>(null)
const editMode = ref(false)

const fetchCases = async () => {
  loading.value = true
  try {
    const response = await api.get('/cases')
    cases.value = response.data
  } catch (err) {
    console.error('Ошибка при загрузке жалоб:', err)
  } finally {
    loading.value = false
  }
}

const openViewModal = async (id: number) => {
  editMode.value = false
  await openModalWithData(id)
}

const openEditModal = async (id: number) => {
  editMode.value = true
  await openModalWithData(id)
}

const openModalWithData = async (id: number) => {
  try {
    const response = await api.get(`/cases/${id}`)
    selectedCase.value = response.data

    const feedbackResponse = await api.get(`/cases/${id}/feedbacks`)
    feedbacks.value = feedbackResponse.data

    showModal.value = true
  } catch (err) {
    alert('Ошибка при загрузке данных жалобы или отзывов')
  }
}

const closeModal = () => {
  showModal.value = false
  selectedCase.value = null
}

const saveCase = async () => {
  if (!selectedCase.value) return

  try {
    const { id, ...payload } = selectedCase.value
    const response = await api.put(`/cases/${id}`, payload)
    selectedCase.value = response.data
    await fetchCases()
    closeModal()
  } catch (err) {
    alert('Ошибка при сохранении изменений')
  }
}

const deleteCase = async (id: number) => {
  if (!confirm('Вы уверены, что хотите удалить жалобу?')) return

  try {
    await api.delete(`/cases/${id}`)
    await fetchCases()
  } catch (err) {
    alert('Ошибка при удалении жалобы')
  }
}

interface Feedback {
  id: number
  message: string
  status: string
}

const feedbacks = ref<Feedback[]>([])



onMounted(fetchCases)
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 2rem auto;
}

.case-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.case-table th, .case-table td {
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  text-align: left;
}

.case-table th {
  background-color: #f4f4f4;
}

button {
  margin: 0 0.3rem;
  padding: 0.4rem 0.7rem;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.modal-content {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  margin-top: 1rem;
}

.modal-content input,
.modal-content textarea {
  padding: 0.5rem;
  margin-top: 0.3rem;
}

.modal-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
}
</style>
