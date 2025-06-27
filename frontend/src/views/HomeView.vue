<template>
  <div class="home-container">
    <!-- Header Section -->
    <header class="header">
      <h1>Добро пожаловать на сайт Антикоррупционных Волонтеров</h1>
      <p>Сайт для волонтеров, помогающих в борьбе с коррупцией и расширяющих свои знания в области правовых и этических стандартов.</p>
    </header>

    <!-- Introduction Section -->
    <section class="intro">
      <h2>О сайте</h2>
      <p>Наши волонтеры играют ключевую роль в выявлении и сообщении фактов о коррупции, а также в обучении и распространении информации среди граждан. Этот сайт предоставляет платформу для эффективной работы с жалобами, а также включает обучающие модули для расширения кругозора.</p>
    </section>

    <!-- Main Features -->
    <section class="features">
      <h2>Основные функции</h2>
      <ul>
        <li><strong>Сообщение о коррупции:</strong> Возможность отправлять информацию о фактах коррупции, помогая бороться с нарушениями.</li>
        <li><strong>Обучение:</strong> Доступ к обучающим материалам, которые помогут вам стать более информированными и эффективными в своей работе.</li>
        <li><strong>Просмотр статистики:</strong> Получайте актуальные данные о статусе дел, которые помогут вам лучше понять картину коррупции в вашем регионе.</li>
      </ul>
    </section>

    <!-- Call to Action -->
    <section class="cta" v-if="!isLoggedIn">
      <h2>Начни прямо сейчас!</h2>
      <p>Присоединяйтесь к нам и начните свою работу по борьбе с коррупцией. Зарегистрируйтесь и участвуйте в обучении.</p>
      <button @click="goToSignUp">Стать волонтером</button>
    </section>

    <!-- Footer Section -->
    <footer class="footer">
      <p>&copy; 2025 Антикоррупционные Волонтеры. Все права защищены.</p>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const router = useRouter();

const goToSignUp = () => {
  router.push('/register');  // Здесь предполагается, что у вас есть страница для регистрации
};
</script>

<style scoped>
.home-container {
  font-family: 'Montserrat', sans-serif;
  background: #f7f9fb;
  color: #333;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  color: #1976d2;
}

.header p {
  font-size: 1.2rem;
  color: #555;
}

.intro {
  margin-bottom: 40px;
}

.intro h2 {
  font-size: 2rem;
  color: #1976d2;
}

.features {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 87, 184, 0.1);
}

.features h2 {
  font-size: 1.8rem;
  color: #1976d2;
  margin-bottom: 15px;
}

.features ul {
  list-style-type: none;
  padding-left: 0;
}

.features ul li {
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.cta {
  text-align: center;
  margin-top: 40px;
}

.cta h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.cta button {
  background-color: #1976d2;
  color: #fff;
  padding: 10px 20px;
  font-size: 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cta button:hover {
  background-color: #125ea2;
}

.footer {
  text-align: center;
  margin-top: 40px;
  font-size: 1rem;
  color: #888;
}
</style>
