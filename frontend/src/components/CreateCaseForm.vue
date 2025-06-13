<template>
  <div class="form-container">
    <h1>Сообщить о коррупции</h1>

    <div v-if="message" class="message">{{ message }}</div>

    <select v-model="categoryId" class="select">
      <option disabled value="">Категория жалобы *</option>
      <option v-for="category in categories" :key="category.id" :value="category.id">
        {{ category.name }}
      </option>
    </select>
    <input v-model="title" placeholder="Заголовок *" class="input" />
    <textarea v-model="description" placeholder="Описание" class="textarea"></textarea>

    <select v-model="regionId" class="select">
      <option disabled value="Выберите регион">Выберите регион *</option>
      <option v-for="region in regions" :key="region.id" :value="region.id">
        {{ region.name }}
      </option>
    </select>

    <select v-model="cityId" class="select" :disabled="!regionId">
      <option disabled value="">Выберите город *</option>
      <option v-for="city in filteredCities" :key="city.id" :value="city.id">
        {{ city.name }}
      </option>
    </select>
    <input v-model="address" placeholder="Адрес *" class="input" />
    

    <button @click="submit" :disabled="isSubmitting" class="submit-button">
      {{ isSubmitting ? 'Отправка...' : 'Отправить жалобу' }}
    </button>
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
    title.value = ''
    description.value = ''
    address.value = ''
    regionId.value = null
    cityId.value = null
    categoryId.value = null
  } catch (err) {
    message.value = 'Ошибка при отправке жалобы'
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>


<style scoped>
.form-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
  text-align: center;
  color: #333;
}

.input,
.textarea,
.select {
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 14px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-sizing: border-box;
}

.input:focus,
.textarea:focus,
.select:focus {
  border-color: #42b983;
  outline: none;
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.message {
  color:  #42b983;
  font-size: 14px;
  margin-bottom: 14px;
  text-align: center;
}

.submit-button {
  background-color: #42b983;
  color: white;
  font-size: 16px;
  font-weight: 600;
  padding: 12px;
  width: 100%;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color:  #42b983;
}

.submit-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
</style>
