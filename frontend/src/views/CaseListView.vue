  <template>
    <div class="case-list-container">
      <header class="case-list-header">
        <h1>Мои сообщения о коррупции</h1>
      </header>
      <div class="case-list-toolbar">
        <label for="status-filter">Статус:</label>
        <select id="status-filter" v-model="selectedStatus">
          <option value="">Все</option>
          <option v-for="(label, key) in statusTranslations" :key="key" :value="key">
            {{ label }}
          </option>
        </select>
        <label for="region-filter">Регион:</label>
        <select id="region-filter" v-model="selectedRegion">
          <option value="">Все</option>
          <option v-for="region in uniqueRegions" :key="region" :value="region">
            {{ region }}
          </option>
        </select>

        <label for="city-filter">Город:</label>
        <select id="city-filter" v-model="selectedCity">
          <option value="">Все</option>
          <option v-for="city in filteredCities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
      <div v-if="loading" class="centered-message"><span class="loader"></span> Загрузка...</div>
      <div v-else-if="filteredCases.length === 0" class="centered-message">
        <span>У вас нет жалоб</span>
      </div>

      <div v-else class="case-grid">
        <div v-for="item in filteredCases" :key="item.id" class="case-card">
          <div class="case-card-header">
            <h2>{{ item.title }}</h2>
            <span :class="['status-badge', item.status]">
              {{ statusTranslations[item.status] || item.status }}
            </span>
          </div>
          <div class="case-card-body">
            <div class="case-description">
              {{ item.description }}
            </div>
            <div class="case-address"><i class="fa fa-map-marker-alt"></i> {{ item.address }}</div>
          </div>
          <div class="case-card-actions">
            <button @click="openViewModal(item.id)"><i class="fa fa-eye"></i> Посмотреть</button>
            <template v-if="!['in_review', 'accepted', 'rejected'].includes(item.status)">
              <button @click="openEditModal(item.id)"><i class="fa fa-edit"></i> Изменить</button>
              <button @click="deleteCase(item.id)" class="danger">
                <i class="fa fa-trash"></i> Удалить
              </button>
            </template>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h2 v-if="editMode">Редактировать жалобу</h2>
            <h2 v-else>Просмотр жалобы</h2>
            <button class="modal-close" @click="closeModal">&times;</button>
          </div>
          <div class="modal-content">
            <label>Заголовок:</label>
            <input v-model="selectedCase.title" :readonly="!editMode" />

            <label>Описание:</label>
            <textarea v-model="selectedCase.description" :readonly="!editMode"></textarea>

            <label>Адрес:</label>
            <input v-model="selectedCase.address" :readonly="!editMode" />

            <div v-if="!editMode" class="status-section">
              <span :class="['status-badge', selectedCase.status]">
                {{
                  selectedCase.status === 'accepted'
                    ? '✅ Одобрено'
                    : selectedCase.status === 'rejected'
                      ? '❌ Отказано'
                      : '⏳ В ожидании'
                }}
              </span>
            </div>
            <div
              v-if="!editMode && selectedCase.feedbacks && selectedCase.feedbacks.length > 0"
              class="feedback-section"
            >
              <ul>
                <li v-for="fb in selectedCase.feedbacks" :key="fb.id">
                  <strong>📩 Отзыв:</strong> {{ fb.message }}
                </li>
              </ul>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="closeModal">Закрыть</button>
            <button v-if="editMode" @click="saveCase" class="primary">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script setup lang="ts">
  import { ref, onMounted, computed, watch } from 'vue'
  import api from '@/api/api'
  import { statusTranslations } from '@/constants/statusTranslations'

  interface Case {
    id: number
    title: string
    description: string
    address: string
    status: string
    feedbacks?: Feedback[]
  }
  interface Feedback {
    id: number
    message: string
    status: string
  }

  const selectedStatus = ref('')
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
      const feedbackResponse = await api.get(`/cases/${id}/feedbacks`)
      selectedCase.value = { ...response.data, feedbacks: feedbackResponse.data }
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
      const { id, feedbacks, ...payload } = selectedCase.value
      const response = await api.put(`/cases/${id}`, payload)
      selectedCase.value = { ...response.data, feedbacks: selectedCase.value.feedbacks }
      await fetchCases()
      closeModal()
    } catch (err) {
      alert('Ошибка при сохранении изменений')
    }
  }

  const deleteCase = async (id: number) => {
    if (!confirm('Вы уверены, что хотите удалить?')) return
    try {
      await api.delete(`/cases/${id}`)
      await fetchCases()
    } catch (err) {
      alert('Ошибка при удалении ')
    }
  }

  const selectedRegion = ref('')
  const selectedCity = ref('')

  watch(selectedRegion, () => {
    selectedCity.value = ''
  })

  // Уникальные регионы
  const uniqueRegions = computed(() => {
    const regions = cases.value.map((c) => c.region?.name).filter(Boolean)
    return [...new Set(regions)]
  })

  // Города, зависящие от выбранного региона
  const filteredCities = computed(() => {
    if (!selectedRegion.value) return []
    const cities = cases.value
      .filter((c) => c.region?.name === selectedRegion.value)
      .map((c) => c.city?.name)
      .filter(Boolean)
    return [...new Set(cities)]
  })

  // Общий фильтр
  const filteredCases = computed(() => {
    return cases.value.filter((c) => {
      const statusOk = !selectedStatus.value || c.status === selectedStatus.value
      const regionOk = !selectedRegion.value || c.region?.name === selectedRegion.value
      const cityOk = !selectedCity.value || c.city?.name === selectedCity.value
      return statusOk && regionOk && cityOk
    })
  })

  onMounted(fetchCases)
  </script>

  <style scoped>
  .case-list-container {
    font-family: 'Montserrat', sans-serif;
    max-width: 900px;
    margin: 2.5rem auto;
    padding: 2rem 1.5rem;
    background: #fff;
    border-radius: 18px;
    box-shadow:
      0 4px 24px rgba(0, 87, 184, 0.08),
      0 1.5px 8px rgba(60, 60, 60, 0.07);
  }

  .case-list-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    border-bottom: 1.5px solid #e5eaf2;
    padding-bottom: 1.2rem;
  }

  .case-list-header h1 {
    font-size: 2.1rem;
    font-weight: 700;
    color: #232323;
    margin: 0;
    letter-spacing: 0.01em;
  }

  .case-list-toolbar {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 1.2rem;
    padding: 1rem 1.5rem;
    margin: 2rem 0;
    background: #f9fbfd;
    border-radius: 10px;
    border: 1.5px solid #e5eaf2;
    box-shadow:
      0 1px 6px rgba(0, 87, 184, 0.06),
      0 0.5px 3px rgba(60, 60, 60, 0.05);
    overflow-x: auto; /* ✅ позволяет прокрутку, если экран узкий */
    white-space: nowrap; /* ✅ не переносит элементы */
  }

  .case-list-toolbar label {
    font-weight: 600;
    color: #232323;
    font-size: 1.05rem;
    flex-shrink: 0;
  }

  .case-list-toolbar select {
    padding: 0.45rem 1.1rem;
    border-radius: 6px;
    border: 1.5px solid #cbd5e1;
    background: #fff;
    font-size: 1.05rem;
    color: #232323;
    transition: border 0.2s ease;
    flex-shrink: 0;
  }

  .case-list-toolbar select:focus {
    border: 1.5px solid #0057b8;
    outline: none;
    box-shadow: 0 0 0 3px rgba(0, 87, 184, 0.1);
  }



  .centered-message {
    text-align: center;
    margin: 2.5rem 0;
    font-size: 1.18rem;
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

  .case-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 1.7rem;
  }

  .case-card {
    background: #f9fbfd;
    border-radius: 14px;
    box-shadow: 0 2px 12px rgba(0, 87, 184, 0.07);
    padding: 1.3rem 1.5rem 1.1rem 1.5rem;
    display: flex;
    flex-direction: column;
    transition: box-shadow 0.18s;
    border: 1.5px solid #e5eaf2;
  }

  .case-card:hover {
    box-shadow: 0 6px 24px rgba(0, 87, 184, 0.13);
    border-color: #b3d3f7;
  }

  .case-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.7rem;
  }

  .case-card-header h2 {
    font-size: 1.18rem;
    font-weight: 600;
    color: #232323;
    margin: 0;
  }

  .status-badge {
    padding: 0.23em 1.1em;
    border-radius: 1.2em;
    font-size: 1.01em;
    font-weight: 600;
    color: #fff;
    background: #b3d3f7;
    display: inline-block;
    box-shadow: 0 1px 4px rgba(60, 60, 60, 0.07);
    letter-spacing: 0.01em;
  }

  .status-badge.accepted {
    background: #0057b8;
  }
  .status-badge.in_review {
    background: #f7b731;
    color: #232323;
  }
  .status-badge.rejected {
    background: #eb3b5a;
  }
  .status-badge.pending {
    background: #778ca3;
  }

  .case-card-body {
    margin: 0.7rem 0 0.3rem 0;
  }

  .case-address {
    color: #232323;
    font-size: 0.97em;
    margin-bottom: 0.4em;
    font-weight: 500;
  }

  .case-description {
    color: #232323;
    font-size: 1.01em;
    margin-bottom: 0.3em;
  }

  .case-card-actions {
    display: flex;
    gap: 0.6rem;
    margin-top: 0.7rem;
  }

  button {
    padding: 0.45rem 1.2rem;
    border: none;
    border-radius: 7px;
    background: #0057b8;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    font-size: 1.05rem;
    transition:
      background 0.15s,
      box-shadow 0.15s;
    display: flex;
    align-items: center;
    gap: 0.4em;
    box-shadow: 0 1px 4px rgba(0, 87, 184, 0.07);
  }

  button.danger {
    background: #eb3b5a;
  }

  button.primary {
    background: #0057b8;
  }

  button:hover {
    background: #003e8a;
    box-shadow: 0 2px 8px rgba(0, 87, 184, 0.13);
  }

  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 87, 184, 0.13);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeInBg 0.3s;
  }

  @keyframes fadeInBg {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .modal {
    background: #fff;
    border-radius: 18px;
    box-shadow:
      0 8px 32px rgba(0, 87, 184, 0.13),
      0 1.5px 8px rgba(60, 60, 60, 0.09);
    padding: 2rem 2rem 2rem 2rem;
    width: 480px;
    max-width: 95vw;
    animation: modalPop 0.35s cubic-bezier(0.23, 1.01, 0.32, 1);
    border: 1.5px solid #e5eaf2;
    position: relative;
    overflow: hidden;
  }

  @keyframes modalPop {
    from {
      opacity: 0;
      transform: translateY(40px) scale(0.97);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.3rem;
    border-bottom: 1px solid #e5eaf2;
    padding-bottom: 0.7rem;
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.45rem;
    font-weight: 700;
    color: #232323;
    letter-spacing: 0.01em;
  }

  .modal-close {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: #b3d3f7;
    transition: color 0.18s;
    line-height: 1;
    padding: 0 0.2em;
  }

  .modal-close:hover {
    color: #eb3b5a;
    background: rgba(235, 59, 90, 0.07);
    border-radius: 50%;
  }

  .modal-content {
    display: flex;
    flex-direction: column;
    gap: 1.1rem;
    margin-top: 0.5rem;
    margin-right: 2rem;
  }

  .modal-content label {
    font-weight: 600;
    color: #232323;
    margin-bottom: 0.2rem;
    font-size: 1.02rem;
  }

  .modal-content input,
  .modal-content textarea {
    width: 100%;
    padding: 0.8rem 1rem;
    border: 1.5px solid #e5eaf2;
    border-radius: 7px;
    font-size: 1.04rem;
    background: #f4f8fb;
    transition:
      border 0.18s,
      box-shadow 0.18s;
    margin-bottom: 0.1rem;
    color: #232323;
    outline: none;
    box-shadow: 0 1px 2px rgba(0, 87, 184, 0.03);
  }

  .modal-content input:focus,
  .modal-content textarea:focus {
    border: 1.5px solid #0057b8;
    box-shadow: 0 2px 8px rgba(0, 87, 184, 0.07);
  }

  .modal-content textarea {
    resize: vertical;
    min-height: 110px;
  }

  .status-section {
    margin-top: 0.7rem;
    text-align: right;
  }

  .feedback-section ul {
    list-style: none;
    padding: 0;
  }

  .feedback-section li {
    margin-bottom: 0.5rem;
    padding: 0.7rem 1rem;
    background: #f4f8fb;
    border-radius: 7px;
    color: #232323;
    font-size: 1.01rem;
    box-shadow: 0 1px 3px rgba(0, 87, 184, 0.04);
  }

  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1.1rem;
    margin-top: 1.3rem;
  }

  .modal-actions button {
    padding: 0.6rem 1.4rem;
    border: none;
    border-radius: 7px;
    cursor: pointer;
    font-size: 1.07rem;
    font-weight: 600;
    transition:
      background 0.18s,
      color 0.18s,
      box-shadow 0.18s;
    box-shadow: 0 1px 4px rgba(0, 87, 184, 0.07);
  }

  .modal-actions button:first-child {
    background: #f4f8fb;
    color: #232323;
  }

  .modal-actions button:last-child,
  .modal-actions button.primary {
    background: #0057b8;
    color: white;
  }

  .modal-actions button:hover {
    opacity: 0.93;
    box-shadow: 0 2px 8px rgba(0, 87, 184, 0.13);
  }
  </style>
