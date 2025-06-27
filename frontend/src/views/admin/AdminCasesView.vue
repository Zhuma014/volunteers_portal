<template>
  <div class="container">
    <h1 class="page-title">Все жалобы</h1>

    <!-- Фильтры -->
<div class="filters-row">
  <div class="filter">
    <label for="status-filter">Статус:</label>
    <select id="status-filter" v-model="selectedStatusFilter">
      <option value="">Все</option>
      <option v-for="(label, key) in statusFilterOptions" :key="key" :value="key">
        {{ label }}
      </option>
    </select>
  </div>

  <div class="filter">
    <label for="region-filter">Регион:</label>
    <select id="region-filter" v-model="selectedRegion">
      <option value="">Все</option>
      <option v-for="region in uniqueRegions" :key="region" :value="region">
        {{ region }}
      </option>
    </select>
  </div>

  <div class="filter">
    <label for="city-filter">Город:</label>
    <select id="city-filter" v-model="selectedCity" :disabled="!selectedRegion">
      <option value="">Все</option>
      <option v-for="city in filteredCities" :key="city" :value="city">
        {{ city }}
      </option>
    </select>
  </div>
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

        <p v-if="caseItem.status !== 'submitted'">
          <strong>Статус: </strong>
          <span :class="{
            'status-accepted': caseItem.status === 'accepted',
            'status-rejected': caseItem.status === 'rejected'
          }">
            {{ statusTranslations[caseItem.status] }}
          </span>
        </p>

        <button
          v-if="caseItem.status === 'submitted'"
          @click.stop="startReview(caseItem)"
        >
          Начать рассмотрение
        </button>
      </div>
    </div>

    <!-- Модальное окно -->
    <div v-if="selectedCase" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div style="margin-top: 1rem;">
          <h3>Информация о жалобе</h3>
          <h2>{{ selectedCase.title }}</h2>
          <p><strong>Описание:</strong> {{ selectedCase.description }}</p>
          <p><strong>Категория:</strong> {{ selectedCase.category?.name }}</p>
          <p><strong>Регион:</strong> {{ selectedCase.region?.name }}</p>
          <p><strong>Город:</strong> {{ selectedCase.city?.name }}</p>
          <p><strong>Адрес:</strong> {{ selectedCase.address }}</p>
        </div>

        <div style="margin-top: 1rem;">
          <h3>Информация об авторе</h3>
          <p><strong>ФИО:</strong> {{ selectedCase.owner?.first_name }} {{ selectedCase.owner?.last_name }}</p>
          <p v-if="selectedCase.owner?.phone_number"><strong>Телефон:</strong> {{ selectedCase.owner.phone_number }}</p>
        </div>

        <p><strong>Статус:</strong> {{ statusTranslations[selectedCase.status] }}</p>

        <div v-if="!editMode && selectedCase.feedbacks?.length > 0">
          <p v-for="fb in selectedCase.feedbacks" :key="fb.id">
            <strong>Отзыв:</strong> {{ fb.message }}
          </p>
        </div>

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

        <div v-else class="modal-actions">
          <button @click="closeModal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/api/api'
import { statusTranslations } from '@/constants/statusTranslations'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const statusFilterOptions = computed(() => {
  const map = { ...statusTranslations }
  if (userStore.isAdmin) map.submitted = 'Принято'
  return map
})

interface CaseItem {
  id: number
  title: string
  description: string
  status: string
  region?: { name: string }
  city?: { name: string }
  category?: { name: string }
  owner?: { first_name: string; last_name: string; phone_number?: string }
  address?: string
  feedbacks?: { id: number; message: string }[]
}

const cases = ref<CaseItem[]>([])
const loading = ref(true)
const selectedCase = ref<CaseItem | null>(null)
const selectedStatus = ref('accepted')
const feedbackMessage = ref('')
const selectedStatusFilter = ref('')
const selectedRegion = ref('')
const selectedCity = ref('')

watch(selectedRegion, () => {
  selectedCity.value = ''
})

const uniqueRegions = computed(() => {
  const regions = cases.value.map(c => c.region?.name).filter(Boolean)
  return [...new Set(regions)]
})

const filteredCities = computed(() => {
  if (!selectedRegion.value) return []
  const cities = cases.value
    .filter(c => c.region?.name === selectedRegion.value)
    .map(c => c.city?.name)
    .filter(Boolean)
  return [...new Set(cities)]
})

const filteredCases = computed(() => {
  return cases.value.filter(c => {
    const statusOk = !selectedStatusFilter.value || c.status === selectedStatusFilter.value
    const regionOk = !selectedRegion.value || c.region?.name === selectedRegion.value
    const cityOk = !selectedCity.value || c.city?.name === selectedCity.value
    return statusOk && regionOk && cityOk
  })
})

const handleCardClick = (caseItem: CaseItem) => {
  if (['in_review', 'accepted', 'rejected'].includes(caseItem.status)) {
    openModal(caseItem)
  }
}

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

const startReview = async (caseItem: CaseItem) => {
  try {
    await api.patch(`/staff/cases/${caseItem.id}/status?status=in_review`)
    caseItem.status = 'in_review'
    fetchCases()
  } catch (error) {
    alert('Не удалось начать рассмотрение')
  }
}

const openModal = (caseItem: CaseItem) => {
  selectedCase.value = caseItem
}

const closeModal = () => {
  selectedCase.value = null
  feedbackMessage.value = ''
  selectedStatus.value = 'accepted'
}

const confirmStatusChange = async () => {
  if (!selectedCase.value) return
  try {
    await api.patch(`/staff/cases/${selectedCase.value.id}/status?status=${selectedStatus.value}`)
    await api.post(
      `/staff/cases/${selectedCase.value.id}/feedback`,
      { message: feedbackMessage.value },
      { headers: { 'Content-Type': 'application/json' } }
    )
    closeModal()
    fetchCases()
  } catch (error) {
    console.error('Ошибка:', error)
    alert('Ошибка при обновлении статуса')
  }
}

onMounted(fetchCases)
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 48, 96, 0.05);
  font-family: 'Segoe UI', 'Roboto', sans-serif;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  color: #003366;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e3eaf3;
  padding-bottom: 0.5rem;
}

.filters-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: flex-end;
  margin-bottom: 1.5rem;
}

.filter {
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

label {
  font-weight: 500;
  font-size: 0.95rem;
  color: #1a1a1a;
  margin-bottom: 0.25rem;
}

select,
textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #c2c9d6;
  border-radius: 6px;
  background-color: #fdfdfd;
  font-size: 1rem;
  transition: border-color 0.2s;
}

select:focus,
textarea:focus {
  border-color: #0057b8;
  outline: none;
}

textarea {
  min-height: 80px;
  resize: vertical;
}

button {
  padding: 0.5rem 1.2rem;
  background-color: #0057b8;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

button:hover {
  background-color: #003f88;
}

.case-card {
  border: 1px solid #d3dbe4;
  border-radius: 12px;
  background-color: #ffffff;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease, background-color 0.3s ease;
}

.case-card:hover {
  transform: translateY(-2px);
  background-color: #f5f8fc;
}

.case-card h3 {
  font-size: 1.3rem;
  margin: 0 0 0.5rem;
  color: #002b5c;
  font-weight: 600;
}

.case-card .meta {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.75rem;
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.case-card .meta span {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.case-card .meta strong {
  color: #003366;
}

.case-card p.description {
  font-size: 1rem;
  color: #333;
  margin-top: 1rem;
  line-height: 1.4;
}

.case-card-divider {
  height: 1px;
  background-color: #e4e8ec;
  margin: 1rem 0;
}

.case-card button {
  margin-top: 1rem;
}
.case-card button:hover {
  background-color: #004a7c;
}

.status-accepted {
  color: #2e7d32;
  font-weight: 600;
}

.status-rejected {
  color: #c62828;
  font-weight: 600;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #777;
  padding: 2rem;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 550px;
  max-width: 90%;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.modal h2, .modal h3 {
  margin-top: 0;
  color: #003366;
}

.modal p {
  margin: 0.5rem 0;
  color: #2a2a2a;
  font-size: 0.95rem;
}

.modal-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
