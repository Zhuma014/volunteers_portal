<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { onMounted } from 'vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

onMounted(async () => {
  const token = route.query.token as string
  const canvasToken = route.query.canvas_token as string

  console.log('Получен токен:', token)
  console.log('Canvas token:', canvasToken)

  if (token && canvasToken) {
    try {
      localStorage.setItem('access_token', token) // твой JWT
      localStorage.setItem('canvas_token', canvasToken) // токен Canvas

      await userStore.login(token, canvasToken)
      router.replace('/')
    } catch (e) {
      console.error('Ошибка входа:', e)
      router.replace('/login')
    }
  } else {
    alert('Ошибка: токены не получены')
    router.replace('/login')
  }
})
</script>


<template>
  <div>Авторизация через Canvas... подождите</div>
</template>
