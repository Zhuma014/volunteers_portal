// main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/user' 

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)

const userStore = useUserStore()

if (userStore.isLoggedIn) {
  userStore.fetchUser()
}

app.mount('#app')
