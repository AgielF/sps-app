import axios from 'axios'
import { jwtDecode } from 'jwt-decode'
import { Notify } from 'quasar'

const api = axios.create({
  baseURL: 'https://spsbackend.pythonanywhere.com/api',
})

// Request interceptor untuk menambahkan token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      // Cek token expiry
      try {
        const payload = jwtDecode(token)
        if (payload.exp * 1000 < Date.now()) {
          // Token expired
          localStorage.removeItem('token')
          localStorage.removeItem('userData')
          window.location.href = '/login'
          return Promise.reject(new Error('Token expired'))
        }
        config.headers.Authorization = `Bearer ${token}`
      } catch (error) {
        localStorage.removeItem('token')
        localStorage.removeItem('userData')
        window.location.href = '/login'
        return Promise.reject(error)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor untuk handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      Notify.create({
        message: 'Sesi telah berakhir, silakan login kembali',
        color: 'warning',
        icon: 'warning',
        timeout: 3000,
      })
      localStorage.removeItem('token')
      localStorage.removeItem('userData')
      setTimeout(() => {
        window.location.href = '/login'
      }, 1000)
    }
    return Promise.reject(error)
  },
)

export default api
