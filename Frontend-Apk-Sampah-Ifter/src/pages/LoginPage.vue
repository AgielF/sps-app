<template>
  <div class="login-page">
    <div class="bg-pattern"></div>

    <div class="content">
      <h1 class="title">Suraja<br />Peduli Sampah.</h1>

      <q-card class="login-card">
        <h3>Masuk</h3>

        <q-input
          v-model="username"
          outlined
          placeholder="Username"
          class="mb input-glow"
          bg-color="white"
          :disable="loading"
        >
          <template v-slot:prepend>
            <q-icon name="people" color="primary" />
          </template>
        </q-input>

        <q-input
          v-model="password"
          outlined
          :type="showPwd ? 'text' : 'password'"
          placeholder="Kata Sandi"
          class="mb input-glow"
          bg-color="white"
          :disable="loading"
          @keyup.enter="handleLogin"
        >
          <template v-slot:prepend>
            <q-icon name="lock" color="primary" />
          </template>
          <template v-slot:append>
            <q-icon
              :name="showPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              color="grey"
              @click="showPwd = !showPwd"
            />
          </template>
        </q-input>

        <div class="text-right q-mb-md">
          <span class="link" @click="lupaSandi">Lupa Sandi? Hubungi petugas.</span>
        </div>

        <q-btn
          label="Masuk"
          class="btn-login"
          unelevated
          no-caps
          @click="handleLogin"
          :loading="loading"
          :disable="loading"
        />
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import { useAuth } from 'src/composables/useAuth'
import { useNotify } from 'src/composables/useNotify'

// Setup composables
const router = useRouter()
const { login, loading } = useAuth()
const { notifyError, notifySuccess, notifyInfo } = useNotify()

const username = ref('')
const password = ref('')
const showPwd = ref(false)

// Clear auth data
const clearAuthData = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userData')
  localStorage.removeItem('username')
  localStorage.removeItem('role')
  localStorage.removeItem('user_id')
}

// Redirect berdasarkan role
const redirectByRole = (role) => {
  switch (role) {
    case 'admin':
      router.push('/admin')
      break
    case 'petugas':
      router.push('/petugas')
      break
    case 'warga':
      router.push('/user')
      break
    default:
      router.push('/')
  }
}

// Cek jika sudah login saat halaman dimuat
onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const payload = jwtDecode(token)
      // Cek apakah token masih valid (belum expired)
      if (payload.exp && payload.exp * 1000 > Date.now()) {
        redirectByRole(payload.role)
      } else {
        // Token expired, hapus data auth
        clearAuthData()
      }
    } catch {
      // Token invalid, hapus data auth
      clearAuthData()
    }
  }
})

// Handle login
const handleLogin = async () => {
  // Validasi input
  if (!username.value.trim() || !password.value.trim()) {
    notifyError('Username dan Kata Sandi wajib diisi!')
    return
  }

  try {
    const response = await login({
      username: username.value,
      password: password.value,
    })

    if (response && response.success) {
      notifySuccess(`Selamat datang, ${response.user.nama || response.user.username}!`)
      redirectByRole(response.user.role)
    }
  } catch (error) {
    console.error('Login error:', error)
    notifyError(error.message || 'Login gagal')
  }
}

// Handle lupa sandi
const lupaSandi = () => {
  notifyInfo('Silahkan gunakan tombol "Hubungi Admin" di bawah untuk bantuan reset sandi.')
}
</script>

<style scoped>
.login-page {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #00513b 0%, #006837 50%, #008749 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.bg-pattern {
  position: absolute;
  width: 100%;
  height: 100%;
  background:
    radial-gradient(circle at 10% 20%, rgba(255, 193, 7, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 90% 10%, rgba(0, 229, 255, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 193, 7, 0.1) 0%, transparent 40%);
}

.content {
  position: relative;
  z-index: 1;
  width: 90%;
  max-width: 400px;
  padding: 20px;
}

.title {
  font-size: 48px;
  font-weight: 800;
  color: #ffc107;
  margin: 0 0 48px 0;
  line-height: 1.1;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 32px 24px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.login-card h3 {
  font-size: 28px;
  font-weight: 700;
  color: #006837;
  margin: 0 0 24px 0;
  text-align: center;
}

.mb {
  margin-bottom: 20px;
}

.login-card :deep(.q-field__control) {
  border-radius: 12px;
  background: white;
  transition: box-shadow 0.3s ease;
}

.input-glow:focus-within :deep(.q-field__control) {
  box-shadow: 0 0 0 2px rgba(0, 104, 55, 0.2);
  border-color: #006837;
}

.link {
  color: #006837;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s;
}

.link:hover {
  text-decoration: underline;
  color: #008749;
}

.btn-login {
  width: 100%;
  background: linear-gradient(135deg, #006837 0%, #00513b 100%);
  color: white;
  font-size: 16px;
  font-weight: 600;
  padding: 12px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 104, 55, 0.3);
  transition: transform 0.2s;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 104, 55, 0.4);
}

.btn-login:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-hubungi {
  color: #ffc107;
  font-weight: 600;
  border: 1px dashed #ffc107;
  border-radius: 8px;
  width: 100%;
  transition: all 0.3s;
  padding: 8px;
}

.btn-hubungi:hover:not(:disabled) {
  background-color: rgba(255, 248, 225, 0.3);
  color: #ffa000;
  border-style: solid;
}

.btn-hubungi:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .title {
    font-size: 40px;
    margin-bottom: 32px;
  }

  .login-card {
    padding: 24px 16px;
  }

  .login-card h3 {
    font-size: 24px;
    margin-bottom: 20px;
  }
}

@media (max-width: 400px) {
  .title {
    font-size: 32px;
  }

  .content {
    padding: 10px;
  }
}
</style>
