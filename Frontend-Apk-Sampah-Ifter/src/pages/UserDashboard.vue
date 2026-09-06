<template>
  <q-page class="q-pa-md bg-green-1">
    <!-- Welcome Header -->
    <div class="q-mb-lg">
      <div class="text-h5 text-weight-bold text-dark-green q-mb-xs">Selamat datang, {{ nama }}</div>
      <div class="text-caption text-grey-7">{{ getGreeting() }}</div>
    </div>

    <!-- Pengajuan Status Card -->
    <q-card
      v-if="hasPengajuanAktif"
      flat
      class="status-card q-mb-lg"
      :class="{ 'bg-orange-1': true }"
    >
      <q-card-section class="q-pa-md">
        <div class="row items-center justify-between">
          <div class="col">
            <div class="text-subtitle1 text-weight-bold text-dark">Laporan Pengajuan Anda</div>
            <div class="text-caption text-grey-7 q-mt-xs">Status pengajuan terbaru</div>
          </div>
          <q-btn
            flat
            dense
            round
            icon="close"
            color="grey-7"
            size="sm"
            @click="clearPengajuanData"
          />
        </div>

        <div class="row items-center q-mt-md">
          <q-badge :color="getStatusColor(pengajuanAktif.status)" class="status-badge">
            <q-icon :name="getStatusIcon(pengajuanAktif.status)" size="14px" class="q-mr-xs" />
            {{ getStatusText(pengajuanAktif.status) }}
          </q-badge>
        </div>

        <div class="q-mt-md">
          <div class="row items-center q-gutter-sm q-mb-xs">
            <q-icon name="event" color="primary" size="16px" />
            <div class="text-body2 text-dark">
              {{ formatJadwal(pengajuanAktif.tanggal_jadwal) }}
            </div>
          </div>
          <div class="row items-center q-gutter-sm">
            <q-icon name="recycling" color="primary" size="16px" />
            <div class="text-body2 text-dark">
              {{ pengajuanAktif.jenis_sampah || 'Belum ditentukan' }}
            </div>
          </div>
        </div>

        <div class="text-caption text-grey-7 q-mt-sm">
          <q-icon name="info" size="14px" class="q-mr-xs" />
          {{ getPengajuanMessage(pengajuanAktif.status) }}
        </div>
      </q-card-section>
    </q-card>

    <!-- Jadwal Pengambilan Card - UPDATED TO MATCH TODAY'S STYLE -->
    <q-card flat class="schedule-card q-mb-lg">
      <q-card-section class="q-pa-none">
        <!-- Header dengan icon -->
        <div class="schedule-header q-pa-md bg-green-1">
          <div class="row items-center">
            <q-icon name="calendar_month" color="primary" size="28px" class="q-mr-md" />
            <div>
              <div class="text-subtitle1 text-weight-bold text-dark-green">
                Jadwal Pengambilan Terdekat
              </div>
              <div class="text-caption text-grey-7">Jadwal pengambilan sampah terdekat</div>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="q-pa-md">
          <!-- Tampilan hari ini jika ada -->
          <div v-if="jadwalToday.length > 0" class="today-schedule">
            <div class="row items-center q-mb-sm">
              <q-icon name="today" color="green" size="20px" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold text-dark-green">
                {{ formatDay(jadwalToday[0].tanggal) }}
              </div>
            </div>

            <div class="jadwal-details">
              <div class="detail-item">
                <q-icon name="place" color="grey" size="16px" />
                <div>
                  <div class="text-caption text-grey-7">Lokasi</div>
                  <div class="text-body2 text-weight-medium text-dark">
                    {{ jadwalToday[0].wilayah || 'Area Anda' }}
                  </div>
                </div>
              </div>

              <div class="detail-item">
                <q-icon name="person" color="grey" size="16px" />
                <div>
                  <div class="text-caption text-grey-7">Petugas</div>
                  <div class="text-body2 text-weight-medium text-dark">
                    {{ jadwalToday[0].nama_petugas || 'Menunggu penugasan' }}
                  </div>
                </div>
              </div>

              <div class="detail-item">
                <q-icon name="access_time" color="grey" size="16px" />
                <div>
                  <div class="text-caption text-grey-7">Waktu</div>
                  <div class="text-body2 text-weight-medium text-dark">
                    {{ getPickupTime(jadwalToday[0]) }}
                  </div>
                </div>
              </div>
            </div>

            <q-badge
              :color="getStatusColor(jadwalToday[0].status)"
              class="status-badge-large q-mt-md"
            >
              <q-icon :name="getStatusIcon(jadwalToday[0].status)" size="14px" class="q-mr-xs" />
              {{ jadwalToday[0].status || 'Menunggu penjemputan' }}
            </q-badge>
          </div>

          <!-- Tampilan jadwal terdekat jika tidak ada hari ini -->
          <div v-else-if="jadwalNext" class="next-schedule">
            <div class="row items-center q-mb-sm">
              <q-icon name="calendar_today" color="primary" size="20px" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold text-dark-green">
                {{ formatDay(jadwalNext.tanggal) }}
              </div>
            </div>

            <div class="jadwal-details">
              <div class="detail-item">
                <q-icon name="place" color="grey" size="16px" />
                <div>
                  <div class="text-caption text-grey-7">Lokasi</div>
                  <div class="text-body2 text-weight-medium text-dark">
                    {{ jadwalNext.wilayah || 'Area Anda' }}
                  </div>
                </div>
              </div>

              <div class="detail-item">
                <q-icon name="access_time" color="grey" size="16px" />
                <div>
                  <div class="text-caption text-grey-7">Waktu</div>
                  <div class="text-body2 text-weight-medium text-dark">
                    {{ getPickupTime(jadwalNext) }}
                  </div>
                </div>
              </div>
            </div>

            <div class="text-caption text-grey-7 q-mt-md">
              <q-icon name="info" size="14px" class="q-mr-xs" />
              Jadwal pengambilan berikutnya
            </div>
          </div>

          <!-- Tampilan jika tidak ada jadwal -->
          <div v-else class="no-schedule text-center q-py-lg">
            <q-icon name="event_busy" size="48px" color="grey-4" />
            <div class="text-subtitle2 text-grey-6 q-mt-md">Belum ada jadwal pengambilan</div>
            <div class="text-caption text-grey-5">Jadwal akan muncul ketika ada penugasan</div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Action Button -->
    <div class="action-section">
      <q-btn
        label="Ajukan Pengambilan"
        icon="add"
        size="lg"
        class="action-button full-width"
        rounded
        no-caps
        :disable="!canAjukan"
        :loading="loadingAction"
        @click="handleAjukan"
      />

      <div v-if="!canAjukan && jadwalToday.length > 0" class="text-center q-mt-sm">
        <div class="text-caption text-grey-7">Anda sudah mengajukan pengambilan untuk hari ini</div>
      </div>
      <div v-else-if="!canAjukan" class="text-center q-mt-sm">
        <div class="text-caption text-grey-7">
          Pengajuan hanya dapat dilakukan pada hari jadwal pengambilan
        </div>
      </div>
    </div>

    <!-- Jadwal Mendatang (7 Hari) -->
    <div class="q-mt-lg" v-if="jadwalWeek.length > 1">
      <div class="row items-center q-mb-md">
        <q-icon name="schedule" color="green" size="24px" class="q-mr-sm" />
        <div>
          <div class="text-h6 text-weight-bold text-dark-green">Jadwal Mendatang</div>
          <div class="text-caption text-grey-7">7 hari ke depan</div>
        </div>
      </div>

      <div class="row q-col-gutter-sm">
        <div v-for="jadwal in jadwalWeek" :key="jadwal.id" class="col-12">
          <q-card
            flat
            class="jadwal-mendatang-card q-mb-xs"
            :class="{ 'today-card': isToday(jadwal.tanggal) }"
          >
            <q-card-section class="q-pa-sm">
              <div class="row items-center">
                <div class="col">
                  <div class="row items-center q-gutter-sm">
                    <q-badge
                      :color="isToday(jadwal.tanggal) ? 'primary' : 'grey'"
                      class="date-badge"
                    >
                      {{ formatDateBadge(jadwal.tanggal) }}
                    </q-badge>
                    <div class="text-weight-medium">{{ jadwal.wilayah }}</div>
                  </div>
                  <div class="text-caption text-grey-7">
                    {{ jadwal.jam_mulai }} - {{ jadwal.jam_selesai }}
                  </div>
                  <div v-if="jadwal.nama_petugas" class="text-caption text-blue">
                    <q-icon name="person" size="12px" /> {{ jadwal.nama_petugas }}
                  </div>
                </div>
                <div class="col-auto">
                  <div
                    class="text-caption text-center"
                    :class="isToday(jadwal.tanggal) ? 'text-primary' : 'text-grey-7'"
                  >
                    {{ getDaysUntil(jadwal.tanggal) }}
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Dialog Konfirmasi -->
    <q-dialog v-model="showDialog" persistent>
      <q-card class="dialog-card">
        <q-card-section class="text-center">
          <q-avatar color="primary-1" text-color="primary" size="lg" class="q-mb-sm">
            <q-icon name="recycling" />
          </q-avatar>
          <div class="text-h6 text-weight-bold text-dark-green q-mb-sm">
            Apakah Sampah Sudah Dipilah?
          </div>
          <div class="text-body2 text-grey-7 q-mb-md">
            Pastikan sampah sudah dipilah sesuai jenisnya (organik, anorganik, B3) sebelum
            pengambilan.
          </div>
        </q-card-section>

        <q-card-actions align="center" class="q-pb-md">
          <q-btn
            label="Belum, Batal"
            flat
            color="grey"
            @click="showDialog = false"
            class="q-px-lg"
          />
          <q-btn
            label="Sudah, Lanjut"
            color="primary"
            unelevated
            @click="goToLaporan"
            class="q-px-lg"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { date } from 'quasar'
import axios from 'axios'

const router = useRouter()
const API_URL = 'https://spsbackend.pythonanywhere.com/'

// State
const showDialog = ref(false)
const nama = ref('')
const wilayah = ref('')
const loadingAction = ref(false)
const jadwalToday = ref([])
const jadwalWeek = ref([])
const pengajuanList = ref([])
const loading = ref(false)

// Computed
const pengajuanAktif = computed(() => {
  if (pengajuanList.value.length > 0) {
    return (
      pengajuanList.value.find((p) => p.status === 'menunggu' || p.status === 'diproses') ||
      pengajuanList.value[0]
    )
  }
  return null
})

const hasPengajuanAktif = computed(() => {
  return (
    pengajuanAktif.value &&
    (pengajuanAktif.value.status === 'menunggu' || pengajuanAktif.value.status === 'diproses')
  )
})

const jadwalNext = computed(() => {
  if (jadwalWeek.value.length > 0) {
    // Cari jadwal pertama yang bukan hari ini
    for (const jadwal of jadwalWeek.value) {
      if (!isToday(jadwal.tanggal)) {
        return jadwal
      }
    }
  }
  return null
})

const canAjukan = computed(() => {
  if (!jadwalToday.value || jadwalToday.value.length === 0) return false
  if (hasPengajuanAktif.value) return false
  return true
})

// Methods
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Selamat pagi!'
  if (hour < 15) return 'Selamat siang!'
  if (hour < 18) return 'Selamat sore!'
  return 'Selamat malam!'
}

const formatJadwal = (dateString) => {
  if (!dateString) return '-'
  try {
    return date.formatDate(dateString, 'dddd, D MMMM YYYY')
  } catch {
    return dateString
  }
}

const formatDay = (dateString) => {
  if (!dateString) return '-'
  try {
    return date.formatDate(dateString, 'dddd, D MMMM')
  } catch {
    return dateString
  }
}

const formatDateBadge = (dateStr) => {
  if (!dateStr) return '-'
  const dateObj = new Date(dateStr)
  const today = new Date()

  if (dateObj.toDateString() === today.toDateString()) return 'HARI INI'

  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  if (dateObj.toDateString() === tomorrow.toDateString()) return 'BESOK'

  return dateObj.toLocaleDateString('id-ID', { weekday: 'short' }).toUpperCase()
}

const isToday = (dateStr) => {
  if (!dateStr) return false
  const dateObj = new Date(dateStr)
  const today = new Date()
  return dateObj.toDateString() === today.toDateString()
}

const getDaysUntil = (dateStr) => {
  if (!dateStr) return ''
  const dateObj = new Date(dateStr)
  const today = new Date()
  const diffTime = dateObj - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Hari ini'
  if (diffDays === 1) return 'Besok'
  return `${diffDays} hari lagi`
}

const getPickupTime = (jadwal) => {
  if (!jadwal) return '-'

  const start = jadwal.jam_mulai ? jadwal.jam_mulai.substring(0, 5) : '08:00'
  const end = jadwal.jam_selesai ? jadwal.jam_selesai.substring(0, 5) : '12:00'

  const hour = parseInt(start.split(':')[0])
  let label = ''
  if (hour < 12) label = 'Pagi'
  else if (hour < 15) label = 'Siang'
  else label = 'Sore'

  return `${label} (${start}-${end})`
}

const getStatusColor = (status) => {
  if (!status) return 'blue'
  const statusLower = status.toLowerCase()
  if (statusLower.includes('selesai') || statusLower.includes('diambil')) return 'green'
  if (statusLower.includes('proses') || statusLower.includes('menunggu')) return 'orange'
  if (statusLower.includes('batal')) return 'red'
  return 'blue'
}

const getStatusIcon = (status) => {
  if (!status) return 'pending'
  const statusLower = status.toLowerCase()
  if (statusLower.includes('selesai') || statusLower.includes('diambil')) return 'check_circle'
  if (statusLower.includes('proses') || statusLower.includes('menunggu')) return 'schedule'
  if (statusLower.includes('batal')) return 'cancel'
  return 'pending'
}

const getStatusText = (status) => {
  if (!status) return 'Menunggu'
  const statusLower = status.toLowerCase()
  if (statusLower.includes('selesai')) return 'Selesai'
  if (statusLower.includes('diproses')) return 'Diproses'
  if (statusLower.includes('menunggu')) return 'Menunggu'
  if (statusLower.includes('batal')) return 'Dibatalkan'
  return status
}

const getPengajuanMessage = (status) => {
  const messages = {
    menunggu: 'Petugas akan menghubungi Anda dalam 1-2 jam',
    diproses: 'Pengambilan sedang diproses',
    selesai: 'Pengambilan telah selesai',
    dibatalkan: 'Pengajuan dibatalkan',
  }
  return messages[status] || 'Menunggu konfirmasi petugas'
}

const clearPengajuanData = () => {
  // Clear pengajuan from store if exists
  fetchPengajuanList()
}

const handleAjukan = () => {
  if (jadwalToday.value.length > 0) {
    showDialog.value = true
  }
}

const goToLaporan = () => {
  showDialog.value = false
  if (jadwalToday.value.length > 0) {
    router.push({
      name: 'UserLaporan',
      query: {
        id_jadwal: jadwalToday.value[0].id,
        tanggal: jadwalToday.value[0].tanggal,
        wilayah: jadwalToday.value[0].wilayah,
      },
    })
  }
}

// Fetch functions
const fetchWargaData = async () => {
  try {
    // Ambil nama dari localStorage
    const userDataStr = localStorage.getItem('userData')
    if (userDataStr) {
      const userData = JSON.parse(userDataStr)
      nama.value = userData.nama || 'Pengguna'
    } else {
      nama.value = 'Pengguna'
    }

    // Wilayah tetap dari API
    const user_id = localStorage.getItem('user_id')
    if (!user_id) {
      wilayah.value = '-'
      return
    }

    const token = localStorage.getItem('token')
    const res = await axios.get(`${API_URL}/api/warga`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: { user_id },
    })

    if (res.data.success && res.data.data.length > 0) {
      wilayah.value = res.data.data[0].wilayah || '-'
    } else {
      wilayah.value = '-'
    }
  } catch (err) {
    console.error(err)
    nama.value = 'Pengguna'
    wilayah.value = '-'
  }
}

const fetchJadwalData = async () => {
  try {
    const token = localStorage.getItem('token')

    // Fetch jadwal hari ini
    const todayRes = await axios.get(`${API_URL}/api/jadwal/today`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (todayRes.data.success) {
      jadwalToday.value = todayRes.data.data || []
    }

    // Fetch jadwal 7 hari ke depan
    const weekRes = await axios.get(`${API_URL}/api/jadwal/week`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (weekRes.data.success) {
      jadwalWeek.value = weekRes.data.data || []
    }
  } catch (err) {
    console.error('Gagal memuat jadwal:', err)
    jadwalToday.value = []
    jadwalWeek.value = []
  }
}

const fetchPengajuanList = async () => {
  try {
    const user_id = localStorage.getItem('user_id')
    if (!user_id) return

    const token = localStorage.getItem('token')

    // Get warga id first
    const wargaRes = await axios.get(`${API_URL}/api/warga`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      params: { user_id: user_id },
    })

    if (!wargaRes.data.success || !wargaRes.data.data || wargaRes.data.data.length === 0) return

    const id_warga = wargaRes.data.data[0].id

    // Get laporan/pengajuan
    const laporanRes = await axios.get(`${API_URL}/api/laporan`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      params: { id_warga: id_warga },
    })

    if (laporanRes.data.success) {
      pengajuanList.value = laporanRes.data.data || []
    }
  } catch (err) {
    console.error('Gagal memuat pengajuan:', err)
    pengajuanList.value = []
  }
}

// Main init
const initDashboard = async () => {
  loading.value = true
  try {
    await Promise.all([fetchWargaData(), fetchJadwalData(), fetchPengajuanList()])
  } catch (err) {
    console.error('Error initializing dashboard:', err)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  initDashboard()
})
</script>

<style scoped>
.text-dark-green {
  color: #08602e !important;
}

/* Status Card */
.status-card {
  border-radius: 16px;
  border-left: 4px solid #ff9800;
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.1);
}

.status-badge {
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
}

/* Schedule Card */
.schedule-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.schedule-header {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border-bottom: 1px solid rgba(0, 104, 55, 0.1);
}

.jadwal-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-item div:last-child {
  flex: 1;
}

.status-badge-large {
  border-radius: 10px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
}

/* Action Section */
.action-section {
  margin-top: 24px;
}

.action-button {
  background: linear-gradient(135deg, #ffd155 0%, #ffca28 100%) !important;
  color: #08602e !important;
  font-weight: 600;
  height: 48px;
  box-shadow: 0 4px 15px rgba(255, 209, 85, 0.3);
  transition: all 0.3s ease;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 209, 85, 0.4);
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Jadwal Mendatang */
.jadwal-mendatang-card {
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  background: white;
  transition: all 0.3s ease;
}

.jadwal-mendatang-card.today-card {
  border: 2px solid #ffca28;
  background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
}

.jadwal-mendatang-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.date-badge {
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 11px;
  font-weight: 600;
  min-width: 60px;
  text-align: center;
}

/* Dialog */
.dialog-card {
  border-radius: 20px;
  min-width: 320px;
  max-width: 400px;
}

/* Jadwal Today dan Next styling konsisten */
.today-schedule,
.next-schedule {
  padding: 8px 0;
}

.no-schedule {
  padding: 32px 0;
}
</style>
