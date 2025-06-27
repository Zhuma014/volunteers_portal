<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleCanvasLogin = () => {
  window.location.href = "http://localhost:8000/api/auth/login/canvas"
}
</script>

<template>
  <div class="login-container">
    <h1>Вход в систему</h1>

    <button @click="handleCanvasLogin" class="canvas-login-button">
      Войти через Canvas
    </button>

    <p class="no-account">
      Нет аккаунта?
      <RouterLink to="/register">Зарегистрируйтесь</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 360px;
  margin: 5vh auto;
  padding: 2.5rem 2rem 2rem 2rem;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  text-align: center;
  font-family: 'Segoe UI', Arial, sans-serif;
}

h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #22223b;
  margin-bottom: 2rem;
  letter-spacing: 0.5px;
}

.canvas-login-button {
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

.canvas-login-button:hover {
  background: linear-gradient(90deg, #0078d4 0%, #005a9c 100%);
}

.no-account {
  margin-top: 2rem;
  font-size: 1rem;
  color: #555;
}

.no-account a {
  color: #005a9c;
  text-decoration: underline;
  font-weight: 500;
  margin-left: 0.3em;
  transition: color 0.2s;
}

.no-account a:hover {
  color: #0078d4;
}
</style>
