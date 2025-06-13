// stores/user.ts
import { defineStore } from 'pinia'
import api from '@/api/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: !!localStorage.getItem('access_token'),
    token: localStorage.getItem('access_token'),
    user: null as null | {
      id: number
      first_name: string
      last_name: string
      role: string
      iin: string
      phone_number?: string
      is_active: boolean
      created_at: string
    },
  }),
  getters: {
    isAdmin: (state) => state.user?.role === 'antikor_staff',
  },
  actions: {
    login(token: string) {
      localStorage.setItem('access_token', token)
      this.token = token
      this.isLoggedIn = true
      this.fetchUser()
    },
    logout() {
      localStorage.removeItem('access_token')
      this.token = null
      this.isLoggedIn = false
      this.user = null
    },
    async fetchUser() {
      if (!this.token) return
      try {
        const res = await api.get('/profile', {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        })
        this.user = res.data
      } catch (err) {
        console.error('Ошибка при загрузке профиля:', err)
        this.logout()
      }
    },
  },
})
