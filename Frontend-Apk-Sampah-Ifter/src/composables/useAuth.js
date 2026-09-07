import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from 'src/utils/axios'

// Global state using Vue reactivity outside component (Simple Store Pattern)
const currentUser = ref(JSON.parse(localStorage.getItem('userData')) || null)
const isAuthenticated = computed(() => !!localStorage.getItem('token'))

export function useAuth() {
  const router = useRouter()
  const loading = ref(false)
  const error = ref(null)

  const login = async (credentials) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/auth/login', credentials)
      if (response.data.success) {
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user_role', response.data.user.role)
        localStorage.setItem('user_id', response.data.user.id)
        localStorage.setItem('userData', JSON.stringify(response.data.user))
        
        currentUser.value = response.data.user
        
        // Routing logic based on Role
        if (response.data.user.role === 'admin') {
          router.push('/admin')
        } else if (response.data.user.role === 'petugas') {
          router.push('/petugas')
        } else {
          router.push('/user')
        }
        return { success: true, user: response.data.user }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed'
      throw new Error(error.value)
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_role')
    localStorage.removeItem('user_id')
    localStorage.removeItem('userData')
    currentUser.value = null
    router.push('/login')
  }

  return {
    currentUser,
    isAuthenticated,
    loading,
    error,
    login,
    logout
  }
}
