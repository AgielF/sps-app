<template>
  <div class="location-tracker">
    <!-- Status Card -->
    <q-card class="q-mb-md shadow-1">
      <q-card-section class="q-pa-sm">
        <div class="row items-center justify-between">
          <div class="col">
            <div class="row items-center">
              <q-avatar
                :color="trackingStatus.color"
                text-color="white"
                size="40px"
                class="q-mr-sm"
              >
                <q-icon :name="trackingStatus.icon" />
              </q-avatar>
              <div>
                <div class="text-subtitle2 text-weight-bold">{{ trackingStatus.title }}</div>
                <div class="text-caption text-grey-7">{{ trackingStatus.subtitle }}</div>
              </div>
            </div>
          </div>
          <div class="col-auto">
            <q-toggle
              v-model="isTracking"
              color="primary"
              :label="isTracking ? 'ON' : 'OFF'"
              :loading="updatingStatus"
              dense
              @update:model-value="toggleTracking"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Location Info -->
    <q-card v-if="isTracking && currentLocation" class="q-mb-md">
      <q-card-section class="q-pa-sm">
        <div class="text-caption text-grey-7">Lokasi saat ini:</div>
        <div class="text-body2 q-mt-xs">
          <q-icon name="location_on" color="primary" size="16px" class="q-mr-xs" />
          {{ currentLocation.latitude.toFixed(6) }}, {{ currentLocation.longitude.toFixed(6) }}
        </div>
        <div class="text-caption text-grey-7 q-mt-xs">
          <q-icon name="schedule" size="12px" class="q-mr-xs" />
          Terakhir: {{ formatTime(lastUpdated) }}
        </div>

        <!-- Additional Info -->
        <div v-if="locationAccuracy" class="row q-mt-sm">
          <div class="col-6">
            <div class="text-caption text-grey-7">Akurasi</div>
            <div class="text-caption text-weight-medium">± {{ locationAccuracy.toFixed(0) }}m</div>
          </div>
          <div class="col-6">
            <div class="text-caption text-grey-7">Update Terakhir</div>
            <div class="text-caption text-weight-medium">
              {{ timeSinceLastUpdate }}
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Stats Card -->
    <q-card v-if="isTracking" class="q-mb-md">
      <q-card-section class="q-pa-sm">
        <div class="text-caption text-grey-7 q-mb-xs">Statistik Tracking</div>
        <div class="row text-center">
          <div class="col-4">
            <div class="text-h6 text-primary">{{ updateCount }}</div>
            <div class="text-caption text-grey-7">Update</div>
          </div>
          <div class="col-4">
            <div class="text-h6 text-green">{{ trackingDuration }}</div>
            <div class="text-caption text-grey-7">Durasi</div>
          </div>
          <div class="col-4">
            <div class="text-h6" :class="lastUpdateStatusClass">
              {{ lastUpdateStatus }}
            </div>
            <div class="text-caption text-grey-7">Status</div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Error Message -->
    <q-banner v-if="error" class="bg-negative text-white q-mt-md">
      <template v-slot:avatar>
        <q-icon name="error" />
      </template>
      {{ errorMessage }}
      <template v-slot:action>
        <q-btn flat label="Coba Lagi" @click="retryConnection" />
      </template>
    </q-banner>

    <!-- GPS Permission Required -->
    <q-dialog v-model="showPermissionDialog" persistent>
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">Izin Lokasi</div>
        </q-card-section>
        <q-card-section>
          <div class="text-body2 q-mb-md">
            Aplikasi memerlukan akses lokasi untuk melacak posisi Anda. Izinkan akses lokasi di
            browser Anda.
          </div>
          <div class="text-caption text-grey-7">
            Pastikan GPS/ lokasi di perangkat Anda sudah aktif.
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Batal" color="grey" @click="showPermissionDialog = false" />
          <q-btn label="Cek Izin" color="primary" @click="checkPermission" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useQuasar, date } from 'quasar'
import api from 'src/services/api'

const $q = useQuasar()

// State
const isTracking = ref(false)
const currentLocation = ref(null)
const locationAccuracy = ref(null)
const lastUpdated = ref(null)
const updateCount = ref(0)
const trackingStartTime = ref(null)
const watchId = ref(null)
const updatingStatus = ref(false)
const error = ref(false)
const errorMessage = ref('')
const showPermissionDialog = ref(false)
const gpsPermission = ref('prompt')

// Computed
const trackingStatus = computed(() => {
  if (!isTracking.value) {
    return {
      title: 'Lokasi Nonaktif',
      subtitle: 'Aktifkan untuk melacak posisi',
      color: 'grey',
      icon: 'location_off',
    }
  }

  if (!currentLocation.value) {
    return {
      title: 'Mencari Lokasi...',
      subtitle: 'Sedang mendapatkan sinyal GPS',
      color: 'orange',
      icon: 'gps_not_fixed',
    }
  }

  const secondsAgo = lastUpdated.value
    ? Math.floor((Date.now() - new Date(lastUpdated.value).getTime()) / 1000)
    : 999

  if (secondsAgo < 30) {
    return {
      title: 'Lokasi Aktif',
      subtitle: 'Posisi real-time',
      color: 'positive',
      icon: 'gps_fixed',
    }
  } else if (secondsAgo < 120) {
    return {
      title: 'Lokasi Tertunda',
      subtitle: 'Sedang memperbarui...',
      color: 'warning',
      icon: 'gps_not_fixed',
    }
  } else {
    return {
      title: 'Sinyal Lemah',
      subtitle: 'Periksa koneksi GPS',
      color: 'negative',
      icon: 'gps_off',
    }
  }
})

const timeSinceLastUpdate = computed(() => {
  if (!lastUpdated.value) return '-'

  const seconds = Math.floor((Date.now() - new Date(lastUpdated.value).getTime()) / 1000)

  if (seconds < 60) return `${seconds} detik lalu`
  if (seconds < 3600) return `${Math.floor(seconds / 60)} menit lalu`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} jam lalu`
  return `${Math.floor(seconds / 86400)} hari lalu`
})

const trackingDuration = computed(() => {
  if (!trackingStartTime.value) return '0m'

  const minutes = Math.floor((Date.now() - trackingStartTime.value) / 60000)
  if (minutes < 60) return `${minutes}m`
  return `${Math.floor(minutes / 60)}j ${minutes % 60}m`
})

const lastUpdateStatus = computed(() => {
  if (!lastUpdated.value) return '-'

  const seconds = Math.floor((Date.now() - new Date(lastUpdated.value).getTime()) / 1000)
  if (seconds < 30) return 'Baik'
  if (seconds < 120) return 'Tertunda'
  return 'Lemah'
})

const lastUpdateStatusClass = computed(() => {
  const status = lastUpdateStatus.value
  if (status === 'Baik') return 'text-positive'
  if (status === 'Tertunda') return 'text-warning'
  return 'text-negative'
})

// Functions
const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  return date.formatDate(new Date(timestamp), 'HH:mm:ss')
}

const checkPermission = async () => {
  try {
    if (!navigator.permissions || !navigator.permissions.query) {
      console.log('Permissions API not supported')
      return 'granted'
    }

    const permission = await navigator.permissions.query({ name: 'geolocation' })
    gpsPermission.value = permission.state

    permission.onchange = () => {
      gpsPermission.value = permission.state
      if (permission.state === 'granted' && isTracking.value) {
        startWatchingLocation()
      }
    }

    return permission.state
  } catch (err) {
    console.error('Error checking permission:', err)
    return 'prompt'
  }
}

const startWatchingLocation = () => {
  if (watchId.value !== null) {
    navigator.geolocation.clearWatch(watchId.value)
  }

  if (!navigator.geolocation) {
    error.value = true
    errorMessage.value = 'Browser tidak mendukung geolocation'
    return
  }

  console.log('🛰️ Starting location watch...')

  watchId.value = navigator.geolocation.watchPosition(
    // Success callback
    async (position) => {
      console.log('📍 Location update received:', position.coords)

      currentLocation.value = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
      }
      locationAccuracy.value = position.coords.accuracy
      lastUpdated.value = new Date().toISOString()
      updateCount.value++

      // Send to server
      await sendLocationToServer({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        speed: position.coords.speed || null,
        heading: position.coords.heading || null,
        battery_level: null, // Can't get battery level in web
      })
    },
    // Error callback
    (err) => {
      console.error('❌ Geolocation error:', err)
      error.value = true

      switch (err.code) {
        case err.PERMISSION_DENIED:
          errorMessage.value = 'Izin lokasi ditolak. Aktifkan di pengaturan browser.'
          showPermissionDialog.value = true
          break
        case err.POSITION_UNAVAILABLE:
          errorMessage.value = 'Informasi lokasi tidak tersedia. Pastikan GPS aktif.'
          break
        case err.TIMEOUT:
          errorMessage.value = 'Waktu permintaan lokasi habis.'
          break
        default:
          errorMessage.value = 'Gagal mendapatkan lokasi.'
      }

      // Stop tracking on error
      if (isTracking.value) {
        toggleTracking(false)
      }
    },
    // Options
    {
      enableHighAccuracy: true,
      maximumAge: 30000, // Cache 30 detik
      timeout: 15000, // Timeout 15 detik
    },
  )
}

const sendLocationToServer = async (locationData) => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found')
      return
    }

    const response = await api.post('/api/petugas/update-location', locationData, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (response.data.success) {
      console.log('✅ Location sent to server:', response.data.data)
    } else {
      console.error('❌ Server error:', response.data.message)
    }
  } catch (err) {
    console.error('❌ Failed to send location:', err)
  }
}

const toggleTracking = async (value) => {
  updatingStatus.value = true

  try {
    if (value) {
      // Start tracking
      const permission = await checkPermission()

      if (permission !== 'granted') {
        showPermissionDialog.value = true
        isTracking.value = false
        return
      }

      // Set online status
      await setOnlineStatus(true)

      // Start watching
      startWatchingLocation()
      trackingStartTime.value = Date.now()
      isTracking.value = true

      $q.notify({
        type: 'positive',
        message: 'Tracking lokasi diaktifkan',
        timeout: 2000,
      })
    } else {
      // Stop tracking
      if (watchId.value !== null) {
        navigator.geolocation.clearWatch(watchId.value)
        watchId.value = null
      }

      // Set offline status
      await setOnlineStatus(false)

      currentLocation.value = null
      isTracking.value = false

      $q.notify({
        type: 'info',
        message: 'Tracking lokasi dimatikan',
        timeout: 2000,
      })
    }
  } catch (err) {
    console.error('Error toggling tracking:', err)
    $q.notify({
      type: 'negative',
      message: 'Gagal mengubah status tracking',
      timeout: 3000,
    })
  } finally {
    updatingStatus.value = false
  }
}

const setOnlineStatus = async (isOnline) => {
  try {
    const token = localStorage.getItem('token')
    await api.post(
      '/api/petugas/set-online-status',
      { is_online: isOnline },
      { headers: { Authorization: `Bearer ${token}` } },
    )
  } catch (err) {
    console.error('Failed to set online status:', err)
  }
}

const retryConnection = () => {
  error.value = false
  if (isTracking.value) {
    toggleTracking(false)
    setTimeout(() => toggleTracking(true), 1000)
  }
}

const initialize = async () => {
  // Check if user is petugas
  try {
    const token = localStorage.getItem('token')
    const response = await api.get('/api/petugas/check-status', {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (response.data.success && response.data.is_petugas) {
      // Get current status
      const statusResponse = await api.get('/api/petugas/my-location', {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (statusResponse.data.success && statusResponse.data.data.is_online) {
        isTracking.value = true
        currentLocation.value = {
          latitude: statusResponse.data.data.latitude,
          longitude: statusResponse.data.data.longitude,
        }
        lastUpdated.value = statusResponse.data.data.last_updated

        // Start tracking if was online
        setTimeout(() => {
          if (isTracking.value) {
            startWatchingLocation()
          }
        }, 1000)
      }
    }
  } catch (err) {
    console.log('User is not petugas or error:', err)
  }
}

// Lifecycle
onMounted(() => {
  initialize()
  checkPermission()
})

onBeforeUnmount(() => {
  // Clean up on component unmount
  if (watchId.value !== null) {
    navigator.geolocation.clearWatch(watchId.value)
  }

  // Set offline if still tracking
  if (isTracking.value) {
    setOnlineStatus(false)
  }
})
</script>

<style scoped>
.location-tracker {
  width: 100%;
}

.q-card {
  border-radius: 12px;
}

.text-positive {
  color: #4caf50;
}

.text-warning {
  color: #ff9800;
}

.text-negative {
  color: #f44336;
}
</style>
