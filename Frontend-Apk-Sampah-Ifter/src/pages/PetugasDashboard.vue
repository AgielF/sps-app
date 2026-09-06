<template>
  <q-page class="q-pa-md bg-green-1">
    <!-- HEADER DASHBOARD -->
    <div class="q-mb-lg">
      <div class="text-h4 text-weight-bold text-primary">Dashboard Petugas</div>
      <div class="text-caption text-grey-7">{{ currentDate }} • Monitor aktivitas dan lokasi</div>
    </div>

    <!-- JADWAL & STATISTIK -->
    <q-card flat class="rounded-borders q-mb-md card-status shadow-1">
      <q-card-section class="q-pb-sm">
        <div class="row items-center justify-between">
          <div>
            <div class="text-h6 text-weight-bold text-primary">Jadwal Pengambilan</div>
            <div class="text-caption text-grey-7">
              {{ currentDate }}
              <q-badge v-if="totalKarungHariIni > 0" color="green" class="q-ml-sm">
                {{ totalKarungHariIni }} karung hari ini
              </q-badge>
            </div>
          </div>
          <q-btn
            icon="event"
            :label="jadwalDisplay"
            flat
            dense
            color="primary"
            class="text-weight-medium"
          />
        </div>
      </q-card-section>

      <q-separator />

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner color="primary" size="3em" />
        <div class="text-caption text-grey-7 q-mt-md">Memuat data...</div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center q-pa-lg">
        <q-icon name="error_outline" size="3em" color="negative" />
        <div class="text-h6 text-negative q-mt-md">Gagal memuat data</div>
        <div class="text-caption text-grey-7 q-mt-sm">{{ errorMessage }}</div>
        <q-btn color="primary" label="Coba Lagi" @click="fetchData" class="q-mt-md" />
      </div>

      <!-- Statistik Harian -->
      <div v-if="statistikHariIni" class="row q-col-gutter-sm q-pa-md">
        <div class="col-6">
          <q-card flat class="text-center q-pa-sm bg-blue-1">
            <div class="text-h6 text-weight-bold text-primary">
              {{ statistikHariIni.total_transaksi || 0 }}
            </div>
            <div class="text-caption">Transaksi Hari Ini</div>
          </q-card>
        </div>
        <div class="col-6">
          <q-card flat class="text-center q-pa-sm bg-green-1">
            <div class="text-h6 text-weight-bold text-green-8">
              Rp {{ formatCurrency(statistikHariIni.total_pendapatan || 0) }}
            </div>
            <div class="text-caption">Pendapatan Hari Ini</div>
          </q-card>
        </div>
      </div>

      <!-- Jadwal Hari Ini -->
      <div v-if="jadwalHariIni.length > 0" class="q-pa-md">
        <div class="text-subtitle2 text-weight-bold text-primary q-mb-sm">
          Jadwal Hari Ini ({{ jadwalHariIni.length }})
        </div>

        <q-list separator>
          <q-item
            v-for="jadwal in jadwalHariIni"
            :key="jadwal.id"
            class="bg-blue-1 q-mb-sm rounded-borders"
          >
            <q-item-section avatar>
              <q-avatar color="primary" text-color="white" size="md">
                <q-icon name="schedule" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-bold">{{ jadwal.wilayah }}</q-item-label>
              <q-item-label caption>
                {{ jadwal.jam_mulai }} - {{ jadwal.jam_selesai }}
              </q-item-label>
              <q-item-label caption class="text-blue">
                <q-icon name="people" size="xs" />
                {{ jadwal.nama_petugas || 'Petugas' }}
              </q-item-label>
              <q-item-label caption class="text-green">
                {{ jadwal.tanggal_display }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-badge color="green-7" label="Aktif" />
            </q-item-section>
          </q-item>
        </q-list>
      </div>

      <!-- List Tugas - HANYA JIKA ADA DATA -->
      <div v-if="tugasList.length > 0" class="q-pa-md">
        <div class="row items-center q-mb-sm">
          <div class="text-subtitle2 text-weight-bold text-primary">
            Tugas Pengambilan ({{ tugasList.length }})
          </div>
          <q-space />
          <q-btn
            flat
            dense
            icon="filter_list"
            color="primary"
            size="sm"
            @click="showFilter = !showFilter"
          >
            <q-tooltip>Filter tugas</q-tooltip>
          </q-btn>
        </div>

        <!-- Filter Tugas -->
        <div v-if="showFilter" class="q-mb-md">
          <q-select
            v-model="filterStatus"
            label="Filter Status"
            :options="filterOptions"
            dense
            outlined
            emit-value
            map-options
            class="q-mb-sm"
          />
          <div class="row q-col-gutter-sm">
            <div class="col-6">
              <q-btn
                label="Reset Filter"
                color="grey"
                size="sm"
                unelevated
                class="full-width"
                @click="resetFilter"
              />
            </div>
            <div class="col-6">
              <q-btn
                label="Terapkan"
                color="primary"
                size="sm"
                unelevated
                class="full-width"
                @click="applyFilter"
              />
            </div>
          </div>
        </div>

        <q-list separator>
          <q-item
            v-for="task in filteredTugas"
            :key="task.id"
            :class="{
              'bg-white': task.status === 'Belum diambil',
              'bg-green-1': task.status === 'Sudah diambil',
              'bg-yellow-1': task.status === 'Sedang Diproses',
            }"
            clickable
            v-ripple
            @click="goToForm(task)"
            class="q-py-md"
          >
            <q-item-section avatar>
              <q-avatar :color="getTaskColor(task)" text-color="white" size="md">
                {{ task.type === 'laporan' ? task.name.charAt(0) : 'P' }}
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-bold text-name-color">
                {{ task.name }}
                <q-badge v-if="task.urgent" color="red" class="q-ml-xs">Urgent</q-badge>
              </q-item-label>
              <q-item-label caption>{{ task.address }}</q-item-label>
              <q-item-label caption class="text-blue">
                <q-icon name="recycling" size="xs" />
                {{ task.jenis_sampah }} • estimasi {{ task.jumlah_karung }} karung
                <template v-if="task.estimasi_volume"> • {{ task.estimasi_volume }} </template>
              </q-item-label>
              <q-item-label caption class="text-grey-7 text-caption">
                <q-icon name="access_time" size="xs" />
                {{ task.waktu_laporan }}
              </q-item-label>
            </q-item-section>
            <q-item-section side top>
              <div class="column items-end">
                <q-badge
                  :color="getStatusColor(task.status)"
                  :label="task.status"
                  class="q-mb-xs"
                />
              </div>
            </q-item-section>
          </q-item>
        </q-list>

        <!-- Pagination -->
        <div v-if="tugasList.length > 5" class="text-center q-mt-md">
          <q-pagination
            v-model="currentPage"
            :max="Math.ceil(tugasList.length / pageSize)"
            :max-pages="5"
            direction-links
            boundary-links
            color="primary"
            size="sm"
          />
        </div>
      </div>

      <!-- Empty State - Tidak ada jadwal DAN tidak ada tugas -->
      <div
        v-else-if="jadwalHariIni.length === 0 && tugasList.length === 0"
        class="text-center q-pa-lg"
      >
        <q-icon name="event_busy" size="3em" color="grey-4" class="q-mb-sm" />
        <div class="text-grey-7">Tidak ada jadwal atau tugas untuk hari ini</div>
        <div class="text-caption text-grey-5 q-mt-xs">
          Silakan hubungi administrator untuk penugasan
        </div>
      </div>

      <!-- Empty State - Ada jadwal tapi tidak ada tugas -->
      <div
        v-else-if="tugasList.length === 0 && jadwalHariIni.length > 0"
        class="text-center q-pa-lg"
      >
        <q-icon name="check_circle" size="3em" color="green-4" class="q-mb-sm" />
        <div class="text-grey-7">Tidak ada laporan untuk jadwal ini</div>
        <div class="text-caption text-grey-5 q-mt-xs">
          Mulai patroli untuk mengambil sampah atau tunggu laporan dari warga
        </div>
      </div>
    </q-card>

    <!-- QUICK ACTIONS -->
    <div class="row q-col-gutter-sm q-mb-md">
      <div class="col-4">
        <q-card
          flat
          class="rounded-borders text-center q-pa-sm action-card bg-blue-1"
          clickable
          @click="tambahLaporanManual"
        >
          <q-icon name="add_circle" size="md" color="primary" class="q-mb-xs" />
          <div class="text-caption text-weight-medium">Tambah Laporan</div>
          <div class="text-caption text-grey-7 text-xxs">Manual</div>
        </q-card>
      </div>
      <div class="col-4">
        <q-card
          flat
          class="rounded-borders text-center q-pa-sm action-card bg-green-1"
          clickable
          @click="lihatPeta"
        >
          <q-icon name="map" size="md" color="green-7" class="q-mb-xs" />
          <div class="text-caption text-weight-medium">Lihat Peta</div>
          <div class="text-caption text-grey-7 text-xxs">Wilayah</div>
        </q-card>
      </div>
      <div class="col-4">
        <q-card
          flat
          class="rounded-borders text-center q-pa-sm action-card bg-orange-1"
          clickable
          @click="lihatRiwayat"
        >
          <q-icon name="history" size="md" color="orange-7" class="q-mb-xs" />
          <div class="text-caption text-weight-medium">Riwayat</div>
          <div class="text-caption text-grey-7 text-xxs">Pengambilan</div>
        </q-card>
      </div>
    </div>

    <!-- TOMBOL AKSI UTAMA -->
    <q-card flat class="rounded-borders q-mb-xl card-map shadow-1">
      <q-card-section class="q-pa-md bg-white">
        <div class="text-center q-mb-sm">
          <div class="text-subtitle1 text-weight-bold text-primary">Mulai Pengambilan</div>
          <div class="text-caption text-grey-7">
            {{ getActionLabel() }}
          </div>
        </div>

        <div class="row q-col-gutter-sm">
          <div class="col-6">
            <q-btn
              label="AMBIL DARI LAPORAN"
              color="yellow-8"
              text-color="black"
              unelevated
              class="full-width text-weight-bold q-py-sm"
              :disable="!hasLaporanPending"
              @click="goToLaporanPending"
            />
          </div>
          <div class="col-6">
            <q-btn
              label="MULAI PATROLI"
              color="primary"
              unelevated
              class="full-width text-weight-bold q-py-sm"
              @click="mulaiPatroli"
            />
          </div>
        </div>

        <!-- Info Petugas -->
        <div class="text-center q-mt-md">
          <div class="text-caption text-grey-7">
            Petugas: <strong>{{ petugasNama }}</strong> • ID: {{ petugasId }}
          </div>
          <div v-if="totalKarungPetugas > 0" class="text-caption text-green-7">
            Total karung: {{ totalKarungPetugas }} • Gaji: Rp
            {{ formatCurrency(totalKarungPetugas * 5000) }}
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { date, useQuasar } from 'quasar'
import api from 'src/services/api'
import { useLocationStore } from 'src/stores/locationStore'

const $q = useQuasar()
const router = useRouter()
const locationStore = useLocationStore()

// Data
const today = new Date()
const currentDate = ref(date.formatDate(today, 'DD MMM YYYY'))
const jadwalHariIni = ref([])
const tugasList = ref([])
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')
const showFilter = ref(false)
const filterStatus = ref('all')
const currentPage = ref(1)
const pageSize = 5
const statistikHariIni = ref(null)
const petugasNama = ref('')
const petugasId = ref('')
const totalKarungPetugas = ref(0)
const totalKarungHariIni = ref(0)

// Filter options
const filterOptions = [
  { label: 'Semua Tugas', value: 'all' },
  { label: 'Belum Diambil', value: 'Belum diambil' },
  { label: 'Sedang Diproses', value: 'Sedang Diproses' },
  { label: 'Sudah Diambil', value: 'Sudah diambil' },
]

// Computed
const jadwalDisplay = computed(() => {
  if (jadwalHariIni.value.length === 0) return 'Tidak ada jadwal'
  const jadwal = jadwalHariIni.value[0]
  return `${jadwal.jam_mulai} - ${jadwal.jam_seleshi} (${jadwal.wilayah})`
})

const hasLaporanPending = computed(() => {
  return tugasList.value.some((t) => t.type === 'laporan' && t.status === 'Belum diambil')
})

const getActionLabel = () => {
  if (jadwalHariIni.value.length === 0) {
    return 'Tidak ada jadwal hari ini'
  }

  const pendingCount = tugasList.value.filter(
    (t) => t.type === 'laporan' && t.status === 'Belum diambil',
  ).length
  if (pendingCount > 0) {
    return `Ada ${pendingCount} laporan menunggu pengambilan`
  }
  return 'Mulai patroli rutin sesuai jadwal'
}

const filteredTugas = computed(() => {
  let filtered = tugasList.value

  // Filter berdasarkan status
  if (filterStatus.value !== 'all') {
    filtered = filtered.filter((task) => task.status === filterStatus.value)
  }

  // Pagination
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize

  return filtered.slice(start, end)
})

// Functions
const formatCurrency = (amount) => {
  if (!amount) return '0'
  return new Intl.NumberFormat('id-ID').format(amount)
}

const getTaskColor = (task) => {
  if (task.status === 'Sudah diambil') return 'green'
  if (task.status === 'Sedang Diproses') return 'yellow'
  if (task.type === 'patroli') return 'blue'
  return 'primary'
}

const getStatusColor = (status) => {
  switch (status) {
    case 'Sudah diambil':
      return 'green-7'
    case 'Sedang Diproses':
      return 'yellow-7'
    case 'Belum diambil':
      return 'red-5'
    default:
      return 'grey-6'
  }
}

const resetFilter = () => {
  filterStatus.value = 'all'
  currentPage.value = 1
}

const applyFilter = () => {
  currentPage.value = 1
  showFilter.value = false
}

// Token
const getToken = () => {
  const rawToken = localStorage.getItem('token') || ''
  return rawToken.startsWith('Bearer ') ? rawToken.slice(7) : rawToken
}

// Load data petugas
const loadPetugasData = async () => {
  try {
    const token = getToken()
    const userId = localStorage.getItem('user_id')

    if (!userId) {
      throw new Error('User ID tidak ditemukan')
    }

    // Coba endpoint spesifik
    try {
      const response = await api.get(`/api/petugas/by-user/${userId}`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (response.data.success) {
        const petugas = response.data.data
        localStorage.setItem('petugas_id', petugas.id)
        localStorage.setItem('petugas_nama', petugas.nama_lengkap)
        petugasNama.value = petugas.nama_lengkap
        petugasId.value = petugas.id
        totalKarungPetugas.value = petugas.total_karung || 0
        return true
      }
    } catch {
      console.log('Specific endpoint failed, trying general endpoint...')
    }

    // Coba endpoint general
    try {
      const response = await api.get('/api/petugas', {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (response.data.success && response.data.data) {
        const petugas = response.data.data.find((p) => p.user_id == userId)

        if (petugas) {
          localStorage.setItem('petugas_id', petugas.id)
          localStorage.setItem('petugas_nama', petugas.nama_lengkap)
          petugasNama.value = petugas.nama_lengkap
          petugasId.value = petugas.id
          totalKarungPetugas.value = petugas.total_karung || 0
          return true
        }
      }
    } catch (secondError) {
      console.log('General endpoint failed:', secondError.message)
    }

    // Jika semua gagal, set dari localStorage
    petugasNama.value = localStorage.getItem('petugas_nama') || 'Petugas'
    petugasId.value = localStorage.getItem('petugas_id') || ''
    return false
  } catch (err) {
    console.error('Error loading petugas data:', err)
    errorMessage.value = 'Gagal memuat data petugas'
    return false
  }
}

// Fetch statistik hari ini
const fetchStatistikHariIni = async () => {
  try {
    const token = getToken()
    const petugasId = localStorage.getItem('petugas_id')
    const todayStr = date.formatDate(today, 'YYYY-MM-DD')

    if (!petugasId) return

    const response = await api.get(`/api/transaksi/statistik/petugas/${petugasId}`, {
      headers: { Authorization: `Bearer ${token}` },
      params: { tanggal: todayStr },
    })

    if (response.data.success) {
      statistikHariIni.value = response.data.data
      totalKarungHariIni.value = response.data.data.total_karung || 0
    }
  } catch (error) {
    console.log('Error fetching statistik:', error)
  }
}

// Fetch jadwal petugas hari ini
const fetchJadwal = async () => {
  try {
    const token = getToken()
    const petugasId = localStorage.getItem('petugas_id')

    if (!petugasId) {
      console.log('Petugas ID tidak ditemukan')
      jadwalHariIni.value = []
      return
    }

    const todayStr = date.formatDate(today, 'YYYY-MM-DD')

    const response = await api.get(`/api/jadwal/petugas/${petugasId}`, {
      headers: { Authorization: `Bearer ${token}` },
      params: {
        tanggal: todayStr,
        status: 'aktif',
      },
    })

    if (response.data.success) {
      jadwalHariIni.value = response.data.data || []
    } else {
      console.warn('API response not success:', response.data.message)
      jadwalHariIni.value = []
    }
  } catch (err) {
    console.error('Error fetching jadwal:', err)
    jadwalHariIni.value = []
  }
}

// Fetch laporan berdasarkan jadwal - HANYA DATA REAL, TANPA DEFAULT
const fetchTugas = async () => {
  try {
    const token = getToken()
    const petugasId = localStorage.getItem('petugas_id')

    if (!petugasId) {
      console.log('❌ Petugas ID tidak ditemukan untuk fetch tugas')
      tugasList.value = [] // Kosongkan
      return
    }

    console.log('📡 Fetching tugas untuk petugas:', petugasId)

    // Coba endpoint by petugas
    try {
      const todayStr = date.formatDate(today, 'YYYY-MM-DD')
      console.log('📡 API: /api/laporan/by-petugas/' + petugasId)

      const response = await api.get(`/api/laporan/by-petugas/${petugasId}`, {
        headers: { Authorization: `Bearer ${token}` },
        params: {
          status: 'menunggu,diproses',
          tanggal: todayStr,
        },
      })

      console.log('📦 Response tugas:', response.data)

      if (response.data.success) {
        if (response.data.data && response.data.data.length > 0) {
          // HAPUS SEMUA DEFAULT VALUE - HANYA PAKAI DATA YANG ADA
          tugasList.value = response.data.data
            .map((laporan) => {
              // Validasi: jika nama tidak ada, skip atau kosongkan
              const nama = laporan.nama_pemohon || laporan.nama_warga
              if (!nama || nama.trim() === '') {
                return null // Skip jika tidak ada nama
              }

              return {
                id: laporan.id,
                original_id: laporan.id,
                name: nama, // TIDAK ADA DEFAULT 'Pelanggan'
                address: laporan.alamat_detail || laporan.alamat || '', // Kosong, bukan '-'
                jenis_sampah: laporan.jenis_sampah || '', // Kosong, bukan 'Campuran'
                jumlah_karung: laporan.estimasi_volume || 0, // 0, bukan 1
                estimasi_volume: laporan.estimasi_volume || '',
                status: getStatusDisplay(laporan.status),
                type: 'laporan',
                waktu_laporan: formatWaktu(laporan.tanggal_laporan),
                urgent: laporan.waktu_pengambilan === 'segera',
              }
            })
            .filter((item) => item !== null) // Hapus yang null

          console.log(`✅ Loaded ${tugasList.value.length} tugas REAL dari database`)
        } else {
          tugasList.value = [] // BENAR-BENAR KOSONG
          console.log('ℹ️ Tidak ada laporan ditemukan di database')
        }
      } else {
        console.warn('API response not success:', response.data.message)
        tugasList.value = [] // Kosongkan
      }
    } catch (endpointError) {
      console.log('❌ Endpoint by-petugas gagal:', endpointError.message)
      tugasList.value = [] // Kosongkan jika gagal
    }

    console.log('✅ Final tugas list:', tugasList.value.length, 'items')
  } catch (err) {
    console.error('❌ Error fetching tugas:', err)
    tugasList.value = [] // Kosongkan jika error
  }
}

// Helper functions
const getStatusDisplay = (status) => {
  switch (status) {
    case 'menunggu':
      return 'Belum diambil'
    case 'diproses':
      return 'Sedang Diproses'
    case 'selesai':
      return 'Sudah diambil'
    default:
      return status
  }
}

const formatWaktu = (dateString) => {
  if (!dateString) return ''
  try {
    const dateObj = new Date(dateString)
    const now = new Date()
    const diffHours = Math.floor((now - dateObj) / (1000 * 60 * 60))

    if (diffHours < 1) return 'Baru saja'
    if (diffHours < 24) return `${diffHours} jam yang lalu`

    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays} hari yang lalu`
  } catch {
    return dateString
  }
}

// Navigation functions
const goToForm = (task) => {
  if (task.type === 'laporan') {
    router.push({
      name: 'FormPengambilanSampah',
      query: {
        laporan_id: task.original_id,
        type: 'laporan',
      },
    })
  } else {
    // Jika patroli, arahkan ke form patroli
    router.push({
      name: 'FormPengambilanSampah',
      query: {
        patroli: 'true',
        wilayah: jadwalHariIni.value[0]?.wilayah || 'Wilayah Tugas',
        type: 'patroli',
      },
    })
  }
}

const goToLaporanPending = () => {
  const pendingTask = tugasList.value.find(
    (t) => t.type === 'laporan' && t.status === 'Belum diambil',
  )
  if (pendingTask) {
    goToForm(pendingTask)
  } else {
    $q.notify({
      type: 'info',
      message: 'Tidak ada laporan yang menunggu pengambilan',
      position: 'top',
    })
  }
}

const mulaiPatroli = () => {
  router.push({
    name: 'FormPengambilanSampah',
    query: {
      patroli: 'true',
      wilayah: jadwalHariIni.value[0]?.wilayah || 'Wilayah Tugas',
      type: 'patroli',
    },
  })
}

const tambahLaporanManual = () => {
  $q.dialog({
    title: 'Tambah Laporan Manual',
    message: 'Apakah Anda menemukan sampah yang tidak dilaporkan?',
    cancel: true,
    persistent: true,
    ok: {
      label: 'Ya, Tambah',
      color: 'primary',
    },
  }).onOk(() => {
    router.push({
      name: 'FormPengambilanSampah',
      query: {
        manual: 'true',
        type: 'manual',
      },
    })
  })
}

const lihatPeta = () => {
  router.push({ name: 'PetugasMaps' })
}

const lihatRiwayat = () => {
  router.push({
    name: 'RiwayatPengambilan',
    query: {
      petugas_id: petugasId.value,
      tanggal: date.formatDate(today, 'YYYY-MM-DD'),
    },
  })
}

// Initialize
const fetchData = async () => {
  loading.value = true
  error.value = false
  errorMessage.value = ''

  try {
    await loadPetugasData()
    await fetchJadwal()
    await fetchTugas()
    await fetchStatistikHariIni()
  } catch (err) {
    console.error('Error in fetchData:', err)
    error.value = true
    errorMessage.value = 'Gagal memuat data. Silakan coba lagi.'
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  console.log('🚀 Dashboard mounted')
  fetchData()

  // 🔥 TAMBAHAN INI
  if (!locationStore.isLive) {
    locationStore.startTracking()
  }
})

// Auto-refresh setiap 30 detik
setInterval(() => {
  if (!loading.value) {
    console.log('🔄 Auto-refresh data')
    fetchTugas()
    fetchStatistikHariIni()
  }
}, 30000)
</script>

<style scoped>
.q-page {
  background-color: #f1f8e9 !important;
}

.rounded-borders {
  border-radius: 16px;
}

.text-primary {
  color: #006837 !important;
}

.text-name-color {
  color: #1a237e !important;
}

.q-badge {
  padding: 6px 10px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 11px;
}

.card-status,
.card-map {
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.action-card {
  transition: all 0.2s ease;
  cursor: pointer;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.text-xxs {
  font-size: 0.7rem;
}

/* Shadow untuk card */
.shadow-1 {
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.12),
    0 1px 2px rgba(0, 0, 0, 0.24);
}
</style>
