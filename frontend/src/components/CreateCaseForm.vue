<template>
  <div class="report-container">
    <div v-if="message" class="status-message-top">{{ message }}</div>

    <h1>Сообщить о коррупции</h1>

    <form @submit.prevent="submit" class="report-form">
      <select v-model="categoryId" required class="field">
        <option disabled value="">Категория жалобы *</option>
        <option v-for="category in categories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>

      <input
        v-model="title"
        type="text"
        placeholder="Заголовок *"
        required
        class="field"
      />

      <textarea
        v-model="description"
        placeholder="Описание"
        class="field textarea"
      ></textarea>

      <select v-model="regionId" required class="field">
        <option disabled value="">Выберите регион *</option>
        <option v-for="region in regions" :key="region.id" :value="region.id">
          {{ region.name }}
        </option>
      </select>

      <select v-model="cityId" :disabled="!regionId" required class="field">
        <option disabled value="">Выберите город *</option>
        <option v-for="city in filteredCities" :key="city.id" :value="city.id">
          {{ city.name }}
        </option>
      </select>

      <input
        v-model="address"
        type="text"
        placeholder="Адрес *"
        required
        class="field"
      />

      <button :disabled="isSubmitting" class="submit-button">
        {{ isSubmitting ? 'Отправка...' : 'Отправить жалобу' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/api/api'

const title = ref('')
const description = ref('')
const address = ref('')
const regionId = ref<number | null>(null)
const cityId = ref<number | null>(null)
const categoryId = ref<number | null>(null)

const isSubmitting = ref(false)
const message = ref<string | null>(null)

const regions = ref<{ id: number; name: string }[]>([])
const cities = ref<{ id: number; name: string; region_id: number }[]>([])
const categories = ref<{ id: number; name: string }[]>([])

const filteredCities = computed(() =>
  cities.value.filter((city) => city.region_id === regionId.value)
)

const fetchData = async () => {
  try {
    const [regionRes, cityRes, categoryRes] = await Promise.all([
      api.get('/regions'),
      api.get('/cities'),
      api.get('/categories')
    ])
    regions.value = regionRes.data
    cities.value = cityRes.data
    categories.value = categoryRes.data
  } catch (err) {
    message.value = 'Ошибка при загрузке данных'
    console.error(err)
  }
}

onMounted(fetchData)

watch(regionId, () => {
  cityId.value = null
})

const submit = async () => {
  if (!title.value || !address.value || !regionId.value || !cityId.value || !categoryId.value) {
    message.value = 'Пожалуйста, заполните все обязательные поля'
    setTimeout(() => (message.value = null), 3000) // ← исчезает через 3 секунды
    return
  }

  isSubmitting.value = true
  try {
    await api.post('/cases', {
      title: title.value,
      description: description.value,
      address: address.value,
      region_id: regionId.value,
      city_id: cityId.value,
      category_id: categoryId.value
    })

    message.value = 'Жалоба успешно отправлена'
    setTimeout(() => (message.value = null), 3000) // ← исчезает через 3 секунды

    // Очистка формы
    title.value = ''
    description.value = ''
    address.value = ''
    regionId.value = null
    cityId.value = null
    categoryId.value = null
  } catch (err) {
    message.value = 'Ошибка при отправке жалобы'
    setTimeout(() => (message.value = null), 3000) // ← исчезает через 3 секунды
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}

</script>

<style scoped>
.report-container {
  max-width: 800px;
  margin: 5vh auto;
  padding: 2.5rem 2rem;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', Arial, sans-serif;
}

h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #22223b;
  margin-bottom: 2rem;
  text-align: center;
  letter-spacing: 0.5px;
}

.report-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #f8fafc;
  transition: border 0.2s;
}

.field:focus {
  border: 1.5px solid #2563eb;
  background: #fff;
  outline: none;
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.status-message-top {
  max-width: 400px;
  margin: 0 auto 1.25rem auto;
  padding: 0.85rem 1rem;
  background-color: #f1f5f9;
  border-left: 4px solid #2563eb;
  color: #1e3a8a;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
}

.submit-button {
  width: 100%;
  padding: 0.85rem 0;
  font-size: 1.1rem;
  background: linear-gradient(90deg, #005a9c 0%, #0078d4 100%);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 2px 8px rgba(0,90,156,0.08);
}

.submit-button:hover {
  background: linear-gradient(90deg, #0078d4 0%, #005a9c 100%);
}

.submit-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
</style>
