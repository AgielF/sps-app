<template>
  <q-page class="q-pa-md bg-green-1">
    <div class="text-h6 text-weight-bold text-primary q-mb-sm">Pendapatan Petugas</div>
    <div class="text-caption text-grey-7 q-mb-md">
      Lihat total pendapatan dan aktivitas kerja berdasarkan tanggal.
    </div>

    <!-- Date Picker Card -->
    <q-card flat class="q-pa-sm q-mb-lg date-card" @click="showDatePicker = true">
      <div class="row items-center justify-between cursor-pointer">
        <div class="text-subtitle1 text-grey-8">{{ formattedDate }}</div>
        <q-icon name="event" color="primary" size="sm" />
      </div>
    </q-card>

    <!-- Date Picker Dialog -->
    <q-dialog v-model="showDatePicker" position="bottom">
      <q-date
        v-model="selectedDateModel"
        mask="YYYY-MM-DD"
        :locale="localeOptions"
        :options="dateOptions"
        today-btn
        flat
      />
    </q-dialog>

    <!-- Loading State -->
    <div v-if="loading" class="text-center q-pa-xl">
      <q-spinner color="primary" size="3em" />
      <div class="text-caption text-grey-7 q-mt-md">Memuat data pendapatan...</div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center q-pa-lg">
      <q-icon name="error_outline" size="3em" color="negative" />
      <div class="text-subtitle2 text-negative q-mt-md">Gagal memuat data</div>
      <div class="text-caption text-grey-7 q-mt-sm">{{ errorMessage }}</div>
      <q-btn color="primary" label="Coba Lagi" @click="fetchPendapatan" outline class="q-mt-md" />
    </div>

    <!-- Main Content -->
    <template v-else>
      <q-card flat class="q-pa-md detail-card">
        <q-list separator>
          <q-item-label header class="text-weight-bold text-grey-9"
            >Rincian Pendapatan</q-item-label
          >

          <!-- Income List -->
          <q-item v-for="item in filteredIncome" :key="item.id" class="q-py-sm">
            <q-item-section>
              <q-item-label class="text-weight-medium">{{ item.nama_lengkap }}</q-item-label>
              <q-item-label caption>
                <span v-if="item.wilayah">Wilayah: {{ item.wilayah }}</span>
                <span v-if="item.keterangan"> • {{ item.keterangan }}</span>
              </q-item-label>
              <q-item-label caption class="text-caption text-grey-6">
                {{ formatDate(item.tanggal_bayar) }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <div class="text-weight-bold text-green-8">Rp. {{ formatCurrency(item.gaji) }}</div>
            </q-item-section>
            <q-item-section side>
              <q-icon name="check_circle" color="green-8" size="xs" />
            </q-item-section>
          </q-item>

          <!-- Empty State -->
          <q-item v-if="filteredIncome.length === 0" class="text-center text-grey-5 q-py-lg">
            <q-item-section>
              <q-icon name="payments" size="3em" class="q-mb-sm" />
              <div>Tidak ada pendapatan tercatat pada tanggal ini.</div>
            </q-item-section>
          </q-item>
        </q-list>

        <q-separator class="q-my-md" />

        <!-- Summary Section -->
        <div class="q-pa-sm">
          <div class="row justify-between q-mb-sm">
            <div>Total Gaji :</div>
            <div class="text-weight-bold">Rp. {{ formatCurrency(totalGaji) }}</div>
          </div>

          <q-separator class="q-my-sm" />

          <div class="row justify-between text-h6 text-weight-bold text-primary">
            <div>Total Akhir :</div>
            <div>Rp. {{ formatCurrency(totalAkhir) }}</div>
          </div>

          <!-- Info Petugas -->
          <div class="q-mt-lg bg-blue-grey-1 q-pa-sm rounded-borders">
            <div class="text-caption text-grey-8">
              <q-icon name="info" size="xs" class="q-mr-xs" />
              Informasi Petugas
            </div>
            <div class="text-caption text-grey-7">
              Nama: {{ petugasNama }} • ID: {{ petugasId }}
            </div>
          </div>
        </div>
      </q-card>

      <!-- Monthly Summary -->
      <q-card flat class="q-mt-md q-pa-md">
        <div class="text-subtitle2 text-weight-bold text-grey-8 q-mb-sm">Ringkasan Bulan Ini</div>
        <div class="row justify-between items-center">
          <div class="col">
            <div class="text-caption text-grey-7">Total Pendapatan</div>
            <div class="text-h6 text-primary text-weight-bold">
              Rp. {{ formatCurrency(monthlyTotal) }}
            </div>
          </div>
          <div class="col-auto">
            <div class="text-caption text-grey-7">{{ monthlyCount }} transaksi</div>
          </div>
        </div>
      </q-card>
    </template>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { date } from 'quasar'
import api from 'src/services/api'

// Data
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')
const showDatePicker = ref(false)
const selectedDateModel = ref(date.formatDate(new Date(), 'YYYY-MM-DD'))
const pendapatanList = ref([])
const petugasData = ref(null)

// Computed
const formattedDate = computed(() => {
  return selectedDateModel.value
})

const petugasNama = computed(() => {
  return petugasData.value?.nama_lengkap || localStorage.getItem('petugas_nama') || 'Petugas'
})

const petugasId = computed(() => {
  return petugasData.value?.id || localStorage.getItem('petugas_id') || '-'
})

const filteredIncome = computed(() => {
  if (!pendapatanList.value.length) return []

  return pendapatanList.value.filter((item) => item.tanggal_bayar === selectedDateModel.value)
})

const totalGaji = computed(() => {
  return filteredIncome.value.reduce((sum, item) => sum + (item.gaji || 0), 0)
})

const totalAkhir = computed(() => {
  return totalGaji.value
})

const monthlyTotal = computed(() => {
  if (!pendapatanList.value) return 0

  const today = new Date()
  const firstDay = new Date(today.getFullYear(), today.getMonth(), 1)
  const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0)

  const monthlyData = pendapatanList.value.filter((item) => {
    const itemDate = new Date(item.tanggal_bayar)
    return itemDate >= firstDay && itemDate <= lastDay
  })

  return monthlyData.reduce((sum, item) => sum + (item.gaji || 0), 0)
})

const monthlyCount = computed(() => {
  if (!pendapatanList.value) return 0

  const today = new Date()
  const firstDay = new Date(today.getFullYear(), today.getMonth(), 1)
  const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0)

  return pendapatanList.value.filter((item) => {
    const itemDate = new Date(item.tanggal_bayar)
    return itemDate >= firstDay && itemDate <= lastDay
  }).length
})

// Date Picker Options
const localeOptions = {
  days: ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'],
  daysShort: ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'],
  months: [
    'Januari',
    'Februari',
    'Maret',
    'April',
    'Mei',
    'Juni',
    'Juli',
    'Agustus',
    'September',
    'Oktober',
    'November',
    'Desember',
  ],
  monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
}

const dateOptions = (dateStr) => {
  const dateObj = new Date(dateStr)
  const today = new Date()
  const maxDate = new Date()
  maxDate.setMonth(today.getMonth() + 3) // Allow up to 3 months in future

  return dateObj <= maxDate
}

// Helper Functions
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID').format(amount || 0)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return date.formatDate(dateStr, 'YYYY-MM-DD')
}

const getToken = () => {
  const rawToken = localStorage.getItem('token') || ''
  return rawToken.startsWith('Bearer ') ? rawToken.slice(7) : rawToken
}

// API Functions

const fetchPendapatan = async () => {
  loading.value = true
  error.value = false

  try {
    const token = getToken()

    // Get PETUGAS_ID dari localStorage (bukan user_id!)
    const petugasId = localStorage.getItem('petugas_id') // Ini seharusnya = 1

    console.log('🔍 DEBUG: Petugas ID from localStorage:', petugasId)
    console.log('🔍 DEBUG: User ID from localStorage:', localStorage.getItem('user_id'))

    // Option A: Jika punya endpoint yang menerima petugas_id
    const response = await api.get(`/api/gaji/petugas/${petugasId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    // Option B: Jika punya endpoint yang menerima user_id
    // const userId = localStorage.getItem('user_id')
    // const response = await api.get('/api/gaji/pendapatan/user', {
    //   headers: { Authorization: `Bearer ${token}` },
    //   params: { user_id: userId }
    // })

    console.log('🔍 DEBUG API Response:', response.data)

    if (response.data.success) {
      pendapatanList.value = response.data.data || []
      console.log('✅ Pendapatan loaded:', pendapatanList.value.length, 'records')
    } else {
      throw new Error(response.data.message || 'Gagal memuat data')
    }
  } catch (err) {
    console.error('❌ Error fetching pendapatan:', err)
    console.error('❌ Error response:', err.response?.data)

    error.value = true
    errorMessage.value = err.response?.data?.message || 'Gagal memuat data pendapatan'

    // Fallback untuk testing
    pendapatanList.value = getFallbackData()
    error.value = false
  } finally {
    loading.value = false
  }
}

// Fallback data for testing
const getFallbackData = () => {
  return [
    {
      id: 1,
      petugas_id: 1,
      jadwal_id: 1,
      gaji: 10000,
      tanggal_bayar: date.formatDate(new Date(), 'YYYY-MM-DD'),
      keterangan: 'Gaji patroli pagi',
      nama_lengkap: 'Petugas Contoh',
      wilayah: 'Wilayah Utara',
      periode: date.formatDate(new Date(), 'YYYY-MM-DD'),
    },
    {
      id: 2,
      petugas_id: 1,
      jadwal_id: 2,
      gaji: 15000,
      tanggal_bayar: date.formatDate(new Date(Date.now() - 86400000), 'YYYY-MM-DD'), // Kemarin
      keterangan: 'Gaji tambahan',
      nama_lengkap: 'Petugas Contoh',
      wilayah: 'Wilayah Selatan',
      periode: date.formatDate(new Date(Date.now() - 86400000), 'YYYY-MM-DD'),
    },
  ]
}

// Watchers
watch(selectedDateModel, () => {
  showDatePicker.value = false
})

// Lifecycle
onMounted(() => {
  fetchPendapatan()
})
</script>

<style scoped>
.q-page {
  background-color: #f1f8e9 !important;
}

.text-primary {
  color: #006837 !important;
}

.text-green-8 {
  color: #4caf50 !important;
}

.date-card,
.detail-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.rounded-borders {
  border-radius: 8px;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .text-h6 {
    font-size: 1.25rem;
  }
}
</style>
