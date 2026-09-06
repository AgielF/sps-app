<template>
  <q-layout view="lHh lpr lFf">
    <!-- HEADER -->
    <q-header bordered class="bg-white text-dark q-py-sm header-custom">
      <q-toolbar>
        <q-toolbar-title class="text-h6 text-weight-bold text-primary">
          {{ currentRouteTitle }}
        </q-toolbar-title>

        <!-- Notifikasi Button -->
        <q-btn
          flat
          round
          dense
          icon="notifications_none"
          color="grey-8"
          class="q-mr-sm"
          @click="goToNotifications"
        />

        <!-- User Profile dengan Dropdown -->
        <q-btn-dropdown
          flat
          class="user-profile-btn"
          no-caps
          dropdown-icon="expand_more"
          :menu-offset="[0, 10]"
        >
          <template v-slot:label>
            <div class="row items-center q-gutter-xs no-wrap">
              <div class="user-avatar" :style="avatarColor">
                {{ userInitials }}
              </div>
              <div class="column items-start q-ml-xs">
                <div class="text-subtitle2 text-weight-bold text-dark">{{ userName }}</div>
                <div class="text-caption text-grey-7">{{ userRole }}</div>
              </div>
            </div>
          </template>

          <q-list>
            <q-item clickable v-close-popup @click="showUserInfo">
              <q-item-section avatar>
                <q-icon name="person" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Profil Saya</q-item-label>
                <q-item-label caption>ID: {{ userId }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item clickable v-close-popup @click="handleLogout">
              <q-item-section avatar>
                <q-icon name="logout" color="red" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-red">Keluar</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <!-- MAIN CONTENT -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- FOOTER / BOTTOM NAVIGATION -->
    <q-footer bordered class="bg-white text-primary q-pt-xs footer-custom">
      <q-tabs
        active-color="primary"
        indicator-color="transparent"
        class="text-grey-7"
        align="justify"
        dense
      >
        <q-route-tab to="/petugas" icon="home" label="Dashboard" name="dashboard" exact />
        <q-route-tab to="/petugas/rekap" icon="list_alt" label="Rekap" name="rekap" exact />
        <q-route-tab
          to="/petugas/pendapatan"
          icon="paid"
          label="Pendapatan"
          name="pendapatan"
          exact
        />
      </q-tabs>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'

const route = useRoute()
const $q = useQuasar()

// Data petugas dari localStorage
const userName = ref('')
const userId = ref('')
const userRole = ref('Petugas')
const userWilayah = ref('')

// Load data petugas dari localStorage
const loadUserData = () => {
  const username = localStorage.getItem('username')
  const userIdFromStorage = localStorage.getItem('user_id')
  const role = localStorage.getItem('role')
  const wilayah = localStorage.getItem('wilayah') || ''

  userName.value = username || 'Petugas'
  userId.value = userIdFromStorage || ''
  userRole.value = role ? role.charAt(0).toUpperCase() + role.slice(1) : 'Petugas'
  userWilayah.value = wilayah
}

// Warna avatar berdasarkan huruf pertama username
const avatarColor = computed(() => {
  const colors = [
    'linear-gradient(135deg, #006837, #4CAF50)', // Hijau
    'linear-gradient(135deg, #1976D2, #2196F3)', // Biru
    'linear-gradient(135deg, #7B1FA2, #9C27B0)', // Ungu
    'linear-gradient(135deg, #F57C00, #FF9800)', // Oranye
  ]

  if (userName.value) {
    const firstChar = userName.value.charAt(0).toUpperCase()
    const index = firstChar.charCodeAt(0) % colors.length
    return { background: colors[index] }
  }

  return { background: colors[0] }
})

// Ambil inisial dari nama untuk avatar
const userInitials = computed(() => {
  if (userName.value) {
    // Jika username satu kata, ambil 2 huruf pertama
    if (userName.value.split(' ').length === 1) {
      return userName.value.substring(0, 2).toUpperCase()
    }
    // Jika ada spasi, ambil huruf pertama dari kata pertama dan kedua
    const names = userName.value.split(' ')
    return (names[0][0] + names[names.length - 1][0]).toUpperCase()
  }
  return 'PT'
})

// Judul halaman berdasarkan route
const currentRouteTitle = computed(() => {
  const title = route.meta.title
  if (title) return title

  if (route.path === '/petugas') return 'Dashboard Petugas'
  if (route.path === '/petugas/rekap') return 'Rekap Harian'
  if (route.path === '/petugas/pendapatan') return 'Pendapatan'
  return 'Panel Petugas'
})

const goToNotifications = () => {
  // Tampilkan notifikasi petugas
  $q.dialog({
    title: 'Notifikasi Petugas',
    message: `
      <div class="q-pa-md">
        <div class="text-body2">
          <div class="q-mb-sm">
            <q-icon name="info" color="blue" class="q-mr-sm" />
            <span class="text-weight-medium">Jadwal Hari Ini:</span>
            <div class="text-caption q-ml-md">- Wilayah RT 01 (08:00 - 12:00)</div>
            <div class="text-caption q-ml-md">- Wilayah RT 02 (13:00 - 17:00)</div>
          </div>
          
          <q-separator class="q-my-sm" />
          
          <div class="q-mb-sm">
            <q-icon name="warning" color="orange" class="q-mr-sm" />
            <span class="text-weight-medium">Pengingat:</span>
            <div class="text-caption q-ml-md">- Lapor rekap sebelum jam 18:00</div>
          </div>
          
          <q-separator class="q-my-sm" />
          
          <div class="q-mb-sm">
            <q-icon name="notifications_active" color="green" class="q-mr-sm" />
            <span class="text-weight-medium">Info Terbaru:</span>
            <div class="text-caption q-ml-md">- Meeting petugas: Jumat, 10 Januari</div>
          </div>
        </div>
      </div>
    `,
    html: true,
    ok: {
      color: 'primary',
      label: 'Tutup',
      flat: true,
    },
  })
}

const showUserInfo = () => {
  // Ambil data lengkap petugas
  const namaLengkap = localStorage.getItem('nama_lengkap') || userName.value
  const noTelepon = localStorage.getItem('no_telepon') || '-'
  const wilayah = userWilayah.value || '-'
  const tanggalBergabung = localStorage.getItem('tanggal_bergabung') || '2024-01-01'

  $q.dialog({
    title: 'Profil Petugas',
    message: `
      <div class="q-pa-md">
        <div class="row items-center q-mb-md">
          <div style="width: 60px; height: 60px; border-radius: 50%; background: ${avatarColor.value.background}; color: white; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; margin-right: 16px;">
            ${userInitials.value}
          </div>
          <div>
            <div class="text-h6 text-weight-bold">${namaLengkap}</div>
            <div class="text-caption text-grey-7">${userRole.value}</div>
          </div>
        </div>
        <q-separator class="q-my-sm" />
        <div class="text-body2">
          <div class="row q-mb-xs">
            <div class="col-4 text-grey-7">ID Petugas:</div>
            <div class="col-8 text-weight-medium">${userId.value}</div>
          </div>
          <div class="row q-mb-xs">
            <div class="col-4 text-grey-7">Username:</div>
            <div class="col-8">${userName.value}</div>
          </div>
          <div class="row q-mb-xs">
            <div class="col-4 text-grey-7">Telepon:</div>
            <div class="col-8">${noTelepon}</div>
          </div>
          <div class="row q-mb-xs">
            <div class="col-4 text-grey-7">Wilayah:</div>
            <div class="col-8">${wilayah}</div>
          </div>
          <div class="row q-mb-xs">
            <div class="col-4 text-grey-7">Bergabung:</div>
            <div class="col-8">${new Date(tanggalBergabung).toLocaleDateString('id-ID')}</div>
          </div>
        </div>
      </div>
    `,
    html: true,
    ok: {
      color: 'primary',
      label: 'Tutup',
    },
  })
}

const handleLogout = async () => {
  console.log('Logout process started')

  // Tampilkan konfirmasi dialog
  $q.dialog({
    title: 'Konfirmasi Keluar',
    message: `Apakah Anda yakin ingin keluar dari akun <strong>${userName.value}</strong>?`,
    html: true,
    persistent: true,
    ok: {
      color: 'red',
      label: 'Ya, Keluar',
    },
    cancel: {
      color: 'grey',
      label: 'Batal',
    },
  })
    .onOk(() => {
      console.log('User confirmed logout')

      // Tampilkan loading
      $q.loading.show({
        message: 'Sedang keluar...',
        boxClass: 'bg-grey-2 text-grey-9',
      })

      // 1. Hapus data auth dari localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      localStorage.removeItem('nama_lengkap')
      localStorage.removeItem('no_telepon')
      localStorage.removeItem('alamat')
      localStorage.removeItem('wilayah')
      localStorage.removeItem('tanggal_bergabung')

      console.log('LocalStorage cleared')

      // 2. Hide loading
      $q.loading.hide()

      // 3. Tampilkan notifikasi sukses
      $q.notify({
        type: 'positive',
        message: 'Berhasil keluar dari sistem',
        position: 'top',
        timeout: 1500,
        icon: 'check_circle',
      })

      // 4. Redirect ke halaman login setelah notifikasi
      setTimeout(() => {
        console.log('Redirecting to login page...')
        window.location.href = '/login'
      }, 1000)
    })
    .onCancel(() => {
      console.log('User cancelled logout')
    })
}

// Load user data saat component mounted
onMounted(() => {
  loadUserData()

  // Debug helper
  console.log('PetugasLayout mounted')
  console.log('Current user:', {
    name: userName.value,
    id: userId.value,
    role: userRole.value,
    wilayah: userWilayah.value,
  })
})
</script>

<style scoped>
.text-primary {
  color: #006837 !important;
}
.header-custom {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.footer-custom {
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
  border-top: 1px solid #eee;
}
.q-tabs .q-route-tab--active {
  color: #006837 !important;
}

/* Menyesuaikan font tab untuk 4 item */
:deep(.q-tab__label) {
  font-size: 11px;
  font-weight: 600;
  margin-top: 2px;
  line-height: 1;
}

:deep(.q-tab__icon) {
  font-size: 22px;
  margin-bottom: 2px;
}

/* Styling untuk user profile */
.user-profile-btn {
  padding: 4px 12px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.user-profile-btn:hover {
  background-color: rgba(0, 104, 55, 0.05);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  :deep(.q-tab__label) {
    font-size: 10px;
  }

  :deep(.q-tab__icon) {
    font-size: 20px;
  }

  .user-profile-btn .text-subtitle2 {
    font-size: 11px;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  :deep(.q-tab__label) {
    font-size: 9px;
  }

  :deep(.q-tab__icon) {
    font-size: 18px;
  }

  .user-profile-btn .text-caption {
    display: none;
  }
}
</style>
