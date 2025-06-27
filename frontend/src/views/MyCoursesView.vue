<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import api from '@/api/api'

const activeTab = ref<'waiting' | 'in_progress' | 'ended'>('waiting')
const loading = ref(false)
const error = ref<string | null>(null)
const courses = ref<any[]>([])
const isAdmin = ref(false)

// Получение курсов
const fetchCourses = async () => {
  loading.value = true
  error.value = null
  courses.value = []

  try {
    const token = localStorage.getItem('canvas_token')
    const res = await api.get(`/canvas/enrollments`, {
      headers: {
        'X-Canvas-Token': `Bearer ${token}`,
      },
    })

    isAdmin.value = res.data.is_admin
    courses.value = Array.isArray(res.data.courses) ? res.data.courses : []
  } catch (err: any) {
    console.error('Ошибка загрузки:', err)
    error.value = 'Не удалось загрузить курсы.'
  } finally {
    loading.value = false
  }
}


// Фильтрованные курсы в зависимости от таба и роли
const filteredCourses = computed(() => {
  if (!courses.value) return []

  if (activeTab.value === 'waiting') {
    return courses.value.filter(c =>
      isAdmin.value
        ? c.workflow_state === 'unpublished'
        : c.enrollment_state === 'Ожидает подтверждения'
    )
  }

  if (activeTab.value === 'in_progress') {
    return courses.value.filter(c =>
      isAdmin.value
        ? c.workflow_state === 'available'
        : c.enrollment_state === 'Активный'
    )
  }

  return []
})



const setTab = (tab: typeof activeTab.value) => {
  activeTab.value = tab
}

onMounted(fetchCourses)
watch(activeTab, fetchCourses)

const redirectToCanvas = (courseId: number) => {
  window.location.href = `http://172.23.148.229/courses/${courseId}`
}

const acceptInvitation = async (courseId: number, enrollmentId: number) => {
  const token = localStorage.getItem('canvas_token')
  try {
   await api.post(
  `/canvas/courses/${courseId}/enrollments/${enrollmentId}/accept`,
  null, // тело запроса
  {
    headers: {
      'X-Canvas-Token': token,
    },
  }
)
    await fetchCourses()
  } catch (err) {
    console.error('Ошибка принятия приглашения', err)
  }
}

const rejectInvitation = async (courseId: number, enrollmentId: number) => {
  const token = localStorage.getItem('canvas_token')
  try {
    await api.post(
  `/canvas/courses/${courseId}/enrollments/${enrollmentId}/reject`,
  null,
  {
    headers: {
      'X-Canvas-Token': token,
    },
  }
)
    await fetchCourses()
  } catch (err) {
    console.error('Ошибка отклонения приглашения', err)
  }
}

const handleAccept = async (courseId: number, enrollmentId: number) => {
  const confirmed = window.confirm('Вы уверены, что хотите принять приглашение?')
  if (confirmed) {
    await acceptInvitation(courseId, enrollmentId)
  }
}

const handleReject = async (courseId: number, enrollmentId: number) => {
  const confirmed = window.confirm('Вы уверены, что хотите отклонить приглашение?')
  if (confirmed) {
    await rejectInvitation(courseId, enrollmentId)
  }
}

const selectedCourseId = ref<number | null>(null)
const courseStudents = ref<any[]>([])
const loadingStudents = ref(false)
const showModal = ref(false)

const fetchStudents = async (courseId: number) => {
  selectedCourseId.value = courseId
  loadingStudents.value = true
  try {
    const token = localStorage.getItem('canvas_token')
    const res = await api.get(`/canvas/courses/${courseId}/students`, {
      headers: { 'X-Canvas-Token': token }
    })
    courseStudents.value = res.data.students
    showModal.value = true
  } catch (err) {
    console.error('Ошибка при загрузке студентов:', err)
  } finally {
    loadingStudents.value = false
  }
}

const closeModal = () => {
  showModal.value = false
  selectedCourseId.value = null
  courseStudents.value = []
}

const formatDate = (iso: string | null) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString()
}

</script>


<template>
  <div class="course-list-container">
    <div class="course-list-header">
      <h1>Мои курсы</h1>
    </div>

    <nav class="course-tabs">
      <button :class="{ active: activeTab === 'waiting' }" @click="setTab('waiting')">
        <span class="tab-icon">⏳</span>
        {{ isAdmin ? 'Неопубликованные' : 'Приглашение' }}
      </button>
      <button :class="{ active: activeTab === 'in_progress' }" @click="setTab('in_progress')">
        <span class="tab-icon">📚</span>
        {{ isAdmin ? 'Опубликованные' : 'Активные' }}
      </button>
    </nav>


    <section class="content">
      <div v-if="loading" class="loading">
        <span class="loader"></span>
        <span>Загрузка курсов...</span>
      </div>
      <div v-else-if="error" class="error">
        <span>⚠️ {{ error }}</span>
      </div>
     <div v-else-if="filteredCourses.length === 0" class="empty">
      <span>📭 Курсы не найдены.</span>
    </div>
      <div v-else class="card-grid">
        <div v-for="course in filteredCourses" :key="course.course_id" class="card">
          <div class="card-header">
            <div class="avatar">{{ course.course_name?.charAt(0) || 'К' }}</div>
            <div>
              <h3>{{ course.course_name || 'Без названия' }}</h3>
              <span class="course-code">{{ course.course_code }}</span>
            </div>
          </div>
          <div class="card-body">
            <div class="info-row">
              <span class="label">Роль:</span>
              <span>{{ course.enrollment_type }}</span>
            </div>
            <div class="info-row">
              <span class="label">Статус:</span>
              <span class="status" :class="course.enrollment_state">{{ course.enrollment_state }}</span>
            </div>
            <div class="info-row">
              <span class="label">ID курса:</span>
              <span>{{ course.course_id }}</span>
            </div>
            <div v-if="!isAdmin && activeTab === 'waiting' && course.enrollment_state === 'Ожидает подтверждения'" class="invite-actions">
            <button @click="handleAccept(course.course_id, course.enrollment_id)" class="accept-btn">
  ✅ Принять
</button>

<button @click="handleReject(course.course_id, course.enrollment_id)" class="reject-btn">
  ❌ Отклонить
</button>

          </div>

        <div
          v-if="!isAdmin && activeTab === 'in_progress' && course.progress_percent !== null"
          class="progress-container"
        >
            <div class="progress-label">{{ course.progress_percent }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: course.progress_percent + '%' }"></div>
            </div>
          </div>
      </div>
          <div class="card-footer" v-if="!(activeTab === 'waiting' && !isAdmin)">
  <div class="button-group">
    <button
      class="details-btn"
      @click="redirectToCanvas(course.course_id)"
    >
      Подробнее
    </button>
    <button
v-if="isAdmin && course.workflow_state === 'available'"
  class="details-btn"
  @click="fetchStudents(course.course_id)"
>
  👥 Студенты
</button>

  </div>
</div>


        </div>
      </div>
    </section>
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
  <div class="modal">
    <h2>Студенты курса #{{ selectedCourseId }}</h2>
    <table>
      <thead>
        <tr>
          <th>Имя</th>
          <th>Email</th>
          <th>Дата регистрации</th>
          <th>Последний вход</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in courseStudents" :key="student.id">
          <td>{{ student.name }}</td>
          <td>{{ student.email }}</td>
          <td>{{ formatDate(student.registered_at) }}</td>
          <td>{{ formatDate(student.last_login) }}</td>
        </tr>
      </tbody>
    </table>
    <button class="close-btn" @click="closeModal">Закрыть</button>
  </div>
</div>


  </div>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');


.course-list-container {
  font-family: 'Montserrat', sans-serif;
  max-width: 1100px;
  margin: 2.5rem auto;
  padding: 2rem 1.5rem;
  background: #fff;
  border-radius: 18px;
  box-shadow:
    0 4px 24px rgba(0, 87, 184, 0.08),
    0 1.5px 8px rgba(60, 60, 60, 0.07);
}

.course-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  border-bottom: 1.5px solid #e5eaf2;
  padding-bottom: 1.2rem;
}

.course-list-header h1 {
  font-size: 2.1rem;
  font-weight: 700;
  color: #232323;
  margin: 0;
  letter-spacing: 0.01em;
}

.course-tabs {
  display: flex;
  justify-content: center;
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
  overflow-x: auto;
  white-space: nowrap;
}


.course-tabs button {
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  color: #022549;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.course-tabs button.active {
  background: #1976d2;
  color: #fff;
}



.header h1 {
  margin: 0 0 8px;
  font-size: 2.4rem;
  font-weight: 700;
  color: black
}


.tabs {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 32px 0 24px;
}

.tabs button {
  background: #fff;
  border: none;
  border-radius: 24px;
  padding: 12px 28px;
  font-size: 1rem;
  font-weight: 600;
  color: #1976d2;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.07);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.tabs button.active {
  background: #1976d2;
  color: #fff;
}

.tab-icon {
  font-size: 1.2rem;
}

.content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;
}

.loading,
.error,
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 48px;
  font-size: 1.2rem;
  color: #888;
}

.loader {
  border: 4px solid #e3eaf2;
  border-top: 4px solid #1976d2;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 28px;
  margin-top: 24px;
}

.card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(25, 118, 210, 0.08);
  border: 1px solid #e3eaf2;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.2s ease-in-out;
}

.card:hover {
  box-shadow: 0 6px 24px rgba(25, 118, 210, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px 8px 24px;
  border-bottom: 1px solid #f0f4f8;
}

.avatar {
  background: #1976d2;
  color: #fff;
  font-weight: 700;
  font-size: 1.4rem;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
}

.course-code {
  font-size: 0.95rem;
  color: #1976d2;
  font-weight: 500;
  opacity: 0.8;
}

.card-body {
  padding: 16px 24px 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 1rem;
}

.label {
  color: #888;
  font-weight: 500;
}

.status {
  font-weight: 600;
  text-transform: capitalize;
}
.status.active,
.status.current_and_future {
  color: #388e3c;
}
.status.completed,
.status.concluded {
  color: #1976d2;
}
.status.invited,
.status.creation_pending,
.status.pending {
  color: #fbc02d;
}

.card-footer {
  padding: 12px 24px 20px;
  border-top: 1px solid #f0f4f8;
  display: flex;
  justify-content: flex-end;
}

.details-btn {
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.details-btn:hover {
  background: #125ea2;
}

.progress-container {
  margin-top: 12px;
}

.progress-label {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 6px;
  color: #1976d2;
}

.progress-bar {
  background-color: #e3eaf2;
  border-radius: 12px;
  height: 10px;
  overflow: hidden;
}

.progress-fill {
  background: linear-gradient(90deg, #42b983, #4fd1c5);
  height: 100%;
  width: 0%;
  transition: width 0.3s ease-in-out;
}

.invite-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.accept-btn,
.reject-btn {
  flex: 1;
  padding: 10px 0;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}

.accept-btn {
  background: #4caf50;
  color: white;
}

.accept-btn:hover {
  background: #388e3c;
}

.reject-btn {
  background: #f44336;
  color: white;
}

.reject-btn:hover {
  background: #d32f2f;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 800px;
  width: 90%;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.modal h2 {
  margin-bottom: 1rem;
}

.modal table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.modal table th,
.modal table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}

.close-btn {
  background: #e74c3c;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.button-group {
  display: flex;
  gap: 12px;
}

</style>
