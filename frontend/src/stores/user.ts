// stores/user.ts
import { defineStore } from 'pinia'
import api from '@/api/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: !!localStorage.getItem('access_token'),
    token: localStorage.getItem('access_token'),
    canvasToken: localStorage.getItem('canvas_token'),
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
    async login(token?: string, canvasToken?: string) {
      if (token) {
        localStorage.setItem('access_token', token)
        this.token = token
      }
      if (canvasToken) {
        localStorage.setItem('canvas_token', canvasToken)
        this.canvasToken = canvasToken
      }

      this.isLoggedIn = true
      await this.fetchUser()
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('canvas_token')
      this.token = null
      this.canvasToken = null
      this.isLoggedIn = false
      this.user = null
    },

    async fetchUser() {
      try {
        const res = await api.get('/profile')
        this.user = res.data
      } catch (err) {
        console.error('Ошибка при загрузке профиля:', err)
        this.logout()
      }
    },
  },
})
