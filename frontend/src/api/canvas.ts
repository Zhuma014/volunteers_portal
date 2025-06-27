import axios from 'axios'
import { CANVAS_BASE_URL } from './config'

const canvasApi = axios.create({
  baseURL: CANVAS_BASE_URL,
})

canvasApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('canvas_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default canvasApi
