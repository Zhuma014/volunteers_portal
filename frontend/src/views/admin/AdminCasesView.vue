<template>
  <div class="container">
    <h1 class="page-title">Все жалобы</h1>
<div style="margin: 1rem 0;">
  <label for="status-filter">Фильтровать по статусу:</label>
<select id="status-filter" v-model="selectedStatusFilter">
  <option value="">Все</option>
  <option v-for="(label, key) in statusFilterOptions" :key="key" :value="key">
    {{ label }}
  </option>
</select>
</div>
    <div v-if="loading" class="loading">Загрузка...</div>
    

<div v-else>
  <div
    v-for="caseItem in filteredCases"
    :key="caseItem.id"
    class="case-card"
    @click="handleCardClick(caseItem)"
    style="cursor: pointer"
  >
    <h3>{{ caseItem.title }}</h3>
    <p><strong>Описание:</strong> {{ caseItem.description }}</p>

    <!-- Показываем статус, только если он НЕ submitted -->
    <p v-if="caseItem.status !== 'submitted'">
      <strong>Статус: </strong>
      <span :class="{
        'status-accepted': caseItem.status === 'accepted',
        'status-rejected': caseItem.status === 'rejected'
      }">
        {{ statusTranslations[caseItem.status] }}
      </span>
    </p>

    <!-- Кнопка "Начать рассмотрение" для статуса "submitted" -->
    <button
      v-if="caseItem.status === 'submitted'"
      @click.stop="startReview(caseItem)"
    >
      Начать рассмотрение
    </button>
  </div>
</div>



    <!-- Модальное окно (открывается при нажатии "Посмотреть") -->
    <div v-if="selectedCase" class="modal-overlay" @click.self="closeModal">
  <div class="modal">
    
    <!-- Дополнительная информация о жалобе -->
<div style="margin-top: 1rem;">
  <h3>Информация о жалобе</h3>
  <h2>{{ selectedCase.title }}</h2>
    <p><strong>Описание:</strong> {{ selectedCase.description }}</p>
  <p><strong>Категория:</strong> {{ selectedCase.category?.name }}</p>
  <p><strong>Регион:</strong> {{ selectedCase.region?.name }}</p>
  <p><strong>Город:</strong> {{ selectedCase.city?.name }}</p>
  <p><strong>Адрес:</strong> {{ selectedCase.address}}</p>
</div>

<div style="margin-top: 1rem;">
  <h3>Информация об авторе</h3>
  <p><strong>ФИО:</strong> {{ selectedCase.owner?.first_name }} {{ selectedCase.owner?.last_name }}</p>
  <p v-if="selectedCase.owner?.phone_number"><strong>Телефон:</strong> {{ selectedCase.owner.phone_number }}</p>
</div>
    <p><strong>Статус:</strong> {{ statusTranslations[selectedCase.status] }}</p>
    <p v-if="selectedCase.status === 'accepted' || selectedCase.status === 'rejected'"><div v-if="!editMode && selectedCase.feedbacks && selectedCase.feedbacks.length > 0">

 <p v-for="fb in selectedCase.feedbacks" :key="fb.id">
      <strong>Отзыв:</strong> {{ fb.message }}
    
</p>
</div></p>



    <!-- Форма изменения статуса (если нужно) -->
    <div v-if="selectedCase.status === 'in_review'">
      <label>Изменить статус:
        <select v-model="selectedStatus">
          <option value="accepted">Одобрено</option>
          <option value="rejected">Отклонено</option>
        </select>
      </label>
      <textarea v-model="feedbackMessage" placeholder="Введите обратную связь"></textarea>
      <div class="modal-actions">
        <button @click="confirmStatusChange">Подтвердить</button>
        <button @click="closeModal">Отмена</button>
      </div>
    </div>

    <!-- Добавим кнопку закрытия, если статус не in_review -->
    <div v-else class="modal-actions">
      <button @click="closeModal">Закрыть</button>
    </div>
  </div>
</div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted,computed } from 'vue'
import api from '@/api/api'
import { statusTranslations } from '@/constants/statusTranslations'
import { useUserStore } from '@/stores/user'


const userStore = useUserStore()

const statusFilterOptions = computed(() => {
  const map = { ...statusTranslations }

  if (userStore.isAdmin) {
    map.submitted = 'Принято'
  }

  return map
})


interface CaseItem {
  id: number
  title: string
  description: string
  status: string
}

const cases = ref<CaseItem[]>([])
const loading = ref(true)
const selectedCase = ref<CaseItem | null>(null)
const selectedStatus = ref('accepted')
const feedbackMessage = ref('')
const selectedStatusFilter = ref('')

const filteredCases = computed(() => {
  if (!selectedStatusFilter.value) return cases.value
  return cases.value.filter(c => c.status === selectedStatusFilter.value)
})

const handleCardClick = (caseItem: CaseItem) => {
  if (['in_review', 'accepted', 'rejected'].includes(caseItem.status)) {
    openModal(caseItem)
  }
}
// Загрузка всех жалоб
const fetchCases = async () => {
  try {
    const res = await api.get('/staff/cases')
    cases.value = res.data
  } catch (error) {
    alert('Ошибка при загрузке жалоб')
  } finally {
    loading.value = false
  }
}

// Начать рассмотрение (меняет статус на "in_review")
const startReview = async (caseItem: CaseItem) => {
  try {
    await api.patch(`/staff/cases/${caseItem.id}/status?status=in_review`)
    caseItem.status = 'in_review'
    fetchCases() // Обновляем список
  } catch (error) {
    alert('Не удалось начать рассмотрение')
  }
}

// Открыть модалку с деталями жалобы
const openModal = (caseItem: CaseItem) => {
  selectedCase.value = caseItem
}

// Закрыть модалку
const closeModal = () => {
  selectedCase.value = null
  feedbackMessage.value = ''
  selectedStatus.value = 'accepted'
}

// Подтвердить изменение статуса
const confirmStatusChange = async () => {
  if (!selectedCase.value) return;

  try {
    // 1. Обновляем статус (query param!)
    await api.patch(
      `/staff/cases/${selectedCase.value.id}/status?status=${selectedStatus.value}`
    );

    // 2. Отправляем feedback (в теле JSON)
    await api.post(
      `/staff/cases/${selectedCase.value.id}/feedback`,
      { message: feedbackMessage.value },
      { headers: { "Content-Type": "application/json" } }
    );

    closeModal();
    fetchCases();
  } catch (error) {
    console.error("Ошибка:", error);
    alert("Ошибка при обновлении статуса");
  }
};


onMounted(fetchCases)
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
}

.page-title {
  text-align: center;
  margin-bottom: 2rem;
}

.case-card {
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  background-color: #fafafa;
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #42b983;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
}

.modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}

select, textarea {
  width: 100%;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.status-accepted {
  color: green;
  font-weight: bold;
}

.status-rejected {
  color: red;
  font-weight: bold;
}
</style>
