<template>
  <div class="about-us-container">
    <!-- Header Section -->
    <header class="header">
      <h1>О нас</h1>
      <p>Мы - команда, работающая в области антикоррупционной деятельности, и помогаем волонтерам быть эффективными в борьбе с коррупцией.</p>
    </header>

    <!-- Our Mission -->
    <section class="mission">
      <h2>Наша миссия</h2>
      <p>Нашей главной целью является привлечение активных граждан к борьбе с коррупцией, предоставление инструментов для сообщества для выявления коррупционных схем, а также образование для улучшения общественного сознания.</p>
      <p>Мы стремимся быть эффективными в решении проблем, связанных с коррупцией, и расширить возможности волонтеров для внесения реального вклада в улучшение общества.</p>
    </section>

    <!-- Who We Are -->
    <section class="who-we-are">
      <h2>Кто мы?</h2>
      <p>Мы - группа антикоррупционных активистов и волонтеров, которая объединяет усилия для выявления и сообщения о случаях коррупции. Мы предоставляем ресурсы для обучения и поддержки наших волонтеров, чтобы они могли эффективно выявлять нарушения и помогать в их расследовании.</p>
      <p>Наша команда состоит из опытных специалистов в области права, этики и социальных наук. Мы убеждены, что вместе можем изменить общественные нормы и создать более честное общество.</p>
    </section>

    <!-- What We Do -->
    <section class="what-we-do">
      <h2>Что мы делаем?</h2>
      <ul>
        <li><strong>Обучаем волонтеров:</strong> Мы предоставляем обучающие материалы, тренинги и семинары для волонтеров, чтобы они могли стать экспертами в области прав человека и антикоррупционной деятельности.</li>
        <li><strong>Обрабатываем сообщения:</strong> Наши волонтеры получают и анализируют сообщения о коррупционных действиях, взаимодействуют с компетентными органами и помогают раскрывать правонарушения.</li>
        <li><strong>Собираем и анализируем данные:</strong> Мы поддерживаем платформу для сбора и анализа данных о коррупционных схемах, создавая прозрачную картину ситуации.</li>
        <li><strong>Активно информируем:</strong> Мы делаем доступной информацию для широкой аудитории, чтобы повысить осведомленность о проблемах коррупции и пути их решения.</li>
      </ul>
    </section>

    <!-- Join Us -->
  <section class="join-us" v-if="!isLoggedIn">
      <h2>Присоединяйтесь к нам</h2>
      <p>Мы всегда рады новым волонтерам, готовым бороться с коррупцией. Присоединяйтесь к нашей команде, и вместе мы сможем достичь большего!</p>
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
  router.push('/register');  // Переход на страницу регистрации
};
</script>

<style scoped>
.about-us-container {
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

.mission,
.who-we-are,
.what-we-do {
  margin-bottom: 40px;
}

.mission h2,
.who-we-are h2,
.what-we-do h2 {
  font-size: 2rem;
  color: #1976d2;
}

.mission p,
.who-we-are p {
  font-size: 1.1rem;
  line-height: 1.5;
}

.what-we-do ul {
  list-style-type: none;
  padding-left: 0;
}

.what-we-do li {
  margin-bottom: 20px;
  font-size: 1.1rem;
}

.join-us {
  text-align: center;
  margin-top: 40px;
}

.join-us h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.join-us button {
  background-color: #1976d2;
  color: #fff;
  padding: 10px 20px;
  font-size: 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.join-us button:hover {
  background-color: #125ea2;
}

.footer {
  text-align: center;
  margin-top: 40px;
  font-size: 1rem;
  color: #888;
}
</style>
