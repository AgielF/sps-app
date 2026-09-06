import axios from 'axios'
import { Notify } from 'quasar'

const API_URL = import.meta.env.VITE_API_URL

// Buat instance axios
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (!error.response) {
      Notify.create({
        type: 'negative',
        message: 'Tidak dapat terhubung ke server',
        position: 'top',
      })
      return Promise.reject(error)
    }

    const { status } = error.response

    if (status === 401) {
      Notify.create({
        type: 'warning',
        message: 'Sesi telah berakhir. Silakan login kembali.',
        position: 'top',
      })

      localStorage.removeItem('token')
      localStorage.removeItem('userData')

      setTimeout(() => {
        window.location.href = '#/login'
      }, 1500)
    }

    return Promise.reject(error)
  },
)

export default api

