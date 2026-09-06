<template>
  <q-page class="q-pa-md bg-green-1">
    <!-- HEADER -->
    <div class="row items-center justify-between q-mb-md">
      <div class="text-h6 text-weight-bold text-primary">Rekap Transaksi</div>
      <q-btn round flat icon="refresh" color="primary" @click="fetchRekap" :loading="loading">
        <q-tooltip>Refresh Data</q-tooltip>
      </q-btn>
    </div>

    <!-- FILTER SECTION -->
    <q-card flat class="q-pa-sm q-mb-md filter-card">
      <div class="row items-center q-col-gutter-md">
        <!-- Date Picker -->
        <div class="col-12 col-md-4">
          <q-card flat class="date-card cursor-pointer" @click="showDatePicker = true">
            <div class="row items-center justify-between q-pa-sm">
              <div>
                <div class="text-caption text-grey-7">Tanggal</div>
                <div class="text-subtitle2 text-weight-medium text-dark">{{ formattedDate }}</div>
              </div>
              <q-icon name="event" color="primary" size="sm" />
            </div>
          </q-card>
        </div>

        <!-- Filter Tipe -->
        <div class="col-12 col-md-4">
          <q-select
            v-model="filterType"
            :options="typeOptions"
            label="Tipe Transaksi"
            dense
            outlined
            emit-value
            map-options
            bg-color="white"
            class="filter-select"
          />
        </div>

        <!-- Filter Petugas/Warga -->
        <div class="col-12 col-md-4">
          <q-select
            v-model="filterUser"
            :options="userOptions"
            label="Lihat Data"
            dense
            outlined
            emit-value
            map-options
            bg-color="white"
            class="filter-select"
          />
        </div>
      </div>
    </q-card>

    <!-- Date Picker Dialog -->
    <q-dialog v-model="showDatePicker">
      <q-card class="q-pa-md" style="min-width: 300px">
        <q-card-section>
          <div class="text-h6 text-weight-bold">Pilih Tanggal</div>
        </q-card-section>
        <q-date v-model="selectedDateModel" mask="DD MMM YYYY" />
        <q-card-actions align="right">
          <q-btn flat label="Tutup" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- SUMMARY CARDS -->
    <div class="row q-col-gutter-sm q-mb-md">
      <!-- Total Pemasukan -->
      <div class="col-12 col-sm-4">
        <q-card flat class="summary-card bg-white">
          <div class="row items-center no-wrap">
            <div class="col-auto">
              <q-icon name="trending_up" color="green" size="md" />
            </div>
            <div class="col q-pl-sm">
              <div class="text-subtitle2 text-weight-bold text-green">
                Rp {{ formatCurrency(summary.pemasukan) }}
              </div>
              <div class="text-caption text-grey-7">Total Pemasukan</div>
            </div>
          </div>
        </q-card>
      </div>

      <!-- Total Pengeluaran -->
      <div class="col-12 col-sm-4">
        <q-card flat class="summary-card bg-white">
          <div class="row items-center no-wrap">
            <div class="col-auto">
              <q-icon name="trending_down" color="red" size="md" />
            </div>
            <div class="col q-pl-sm">
              <div class="text-subtitle2 text-weight-bold text-red">
                Rp {{ formatCurrency(summary.pengeluaran) }}
              </div>
              <div class="text-caption text-grey-7">Total Pengeluaran</div>
            </div>
          </div>
        </q-card>
      </div>

      <!-- Saldo Bersih -->
      <div class="col-12 col-sm-4">
        <q-card flat class="summary-card bg-white">
          <div class="row items-center no-wrap">
            <div class="col-auto">
              <q-icon name="account_balance" color="blue" size="md" />
            </div>
            <div class="col q-pl-sm">
              <div class="text-subtitle2 text-weight-bold text-blue">
                Rp {{ formatCurrency(summary.saldo) }}
              </div>
              <div class="text-caption text-grey-7">Saldo Bersih</div>
            </div>
          </div>
        </q-card>
      </div>
    </div>

    <!-- DETAILED STATS -->
    <q-card flat class="q-pa-md q-mb-lg detail-card">
      <div class="text-subtitle1 text-weight-bold text-grey-9 q-mb-md">Statistik Detail</div>

      <div class="row q-col-gutter-md">
        <!-- Transaksi Saya -->
        <div class="col-12 col-sm-6">
          <q-card flat class="stat-card bg-blue-1">
            <div class="q-pa-sm">
              <div class="text-h6 text-weight-bold text-blue">{{ summary.transaksi_saya }}</div>
              <div class="text-caption text-grey-7">Transaksi Saya (Hari Ini)</div>
              <div class="text-caption text-blue q-mt-xs">
                <q-icon name="paid" size="xs" class="q-mr-xs" />
                Rp {{ formatCurrency(summary.pemasukan_saya) }}
              </div>
            </div>
          </q-card>
        </div>

        <!-- Total Transaksi -->
        <div class="col-12 col-sm-6">
          <q-card flat class="stat-card bg-green-1">
            <div class="q-pa-sm">
              <div class="text-h6 text-weight-bold text-green">{{ summary.total_transaksi }}</div>
              <div class="text-caption text-grey-7">Total Transaksi (Semua)</div>
              <div class="text-caption text-green q-mt-xs">
                <q-icon name="receipt" size="xs" class="q-mr-xs" />
                {{ summary.transaksi_lunas }} Lunas, {{ summary.transaksi_pending }} Pending
              </div>
            </div>
          </q-card>
        </div>
      </div>
    </q-card>

    <!-- TRANSACTION TABLE -->
    <q-card flat class="detail-card">
      <q-card-section class="q-pb-none">
        <div class="row items-center justify-between">
          <div class="text-subtitle1 text-weight-bold text-grey-9">Daftar Transaksi</div>
          <div class="text-caption text-grey-7">
            Menampilkan {{ filteredTransactions.length }} transaksi
          </div>
        </div>
      </q-card-section>

      <q-separator class="q-mb-md" />

      <q-card-section class="q-pt-none">
        <q-table
          :rows="filteredTransactions"
          :columns="columns"
          row-key="id"
          flat
          dense
          :pagination="{ rowsPerPage: 10 }"
          class="transaction-table"
        >
          <!-- Custom Body Slot -->
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td key="kode" :props="props">
                <div class="text-caption text-weight-medium">{{ props.row.kode_transaksi }}</div>
                <div class="text-caption text-grey-7">{{ formatTime(props.row.tanggal) }}</div>
              </q-td>

              <q-td key="jenis" :props="props">
                <q-badge
                  :color="props.row.jenis === 'pemasukan' ? 'green' : 'red'"
                  :label="props.row.jenis === 'pemasukan' ? 'Masuk' : 'Keluar'"
                />
                <div class="text-caption text-grey-7 q-mt-xs">{{ props.row.kategori || '-' }}</div>
              </q-td>

              <q-td key="user" :props="props">
                <div v-if="props.row.warga_id">
                  <div class="text-weight-medium">Warga</div>
                  <div class="text-caption text-grey-7">ID: {{ props.row.warga_id }}</div>
                </div>
                <div v-else-if="props.row.petugas_id">
                  <div class="text-weight-medium">Petugas</div>
                  <div class="text-caption text-grey-7">ID: {{ props.row.petugas_id }}</div>
                </div>
                <div v-else class="text-grey-7 text-italic">-</div>
              </q-td>

              <q-td key="jumlah" :props="props">
                <div
                  class="text-subtitle2"
                  :class="props.row.jenis === 'pemasukan' ? 'text-green' : 'text-red'"
                >
                  Rp {{ formatCurrency(props.row.jumlah) }}
                </div>
                <div v-if="props.row.total_karung" class="text-caption text-grey-7">
                  {{ props.row.total_karung }} karung @ Rp
                  {{ formatCurrency(props.row.harga_per_karung) }}
                </div>
              </q-td>

              <q-td key="status" :props="props">
                <q-badge
                  :color="getStatusColor(props.row.status_bayar)"
                  :label="props.row.status_bayar"
                />
                <div class="text-caption text-grey-7 q-mt-xs">{{ props.row.metode_bayar }}</div>
              </q-td>

              <q-td key="keterangan" :props="props">
                <div class="text-caption">{{ props.row.keterangan || '-' }}</div>
              </q-td>
            </q-tr>
          </template>

          <!-- Empty State -->
          <template v-slot:no-data>
            <div class="full-width row flex-center q-pa-lg text-grey-7">
              <q-icon name="receipt" size="xl" class="q-mb-sm" />
              <div class="text-subtitle1 q-ml-sm">Tidak ada transaksi ditemukan</div>
            </div>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { date } from 'quasar'
import api from 'src/services/api'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// UI State
const showDatePicker = ref(false)
const loading = ref(false)
const filterType = ref('semua')
const filterUser = ref('semua')

// Date
const selectedDateModel = ref(date.formatDate(new Date(), 'DD MMM YYYY'))
const selectedDate = computed(() => {
  return date.formatDate(selectedDateModel.value, 'YYYY-MM-DD')
})
const formattedDate = computed(() => selectedDateModel.value)

// Options
const typeOptions = [
  { label: 'Semua Tipe', value: 'semua' },
  { label: 'Pemasukan', value: 'pemasukan' },
  { label: 'Pengeluaran', value: 'pengeluaran' },
  { label: 'Gaji', value: 'gaji' },
  { label: 'Topup', value: 'topup' },
]

const userOptions = [
  { label: 'Semua Data', value: 'semua' },
  { label: 'Transaksi Saya', value: 'saya' },
  { label: 'Transaksi Warga', value: 'warga' },
  { label: 'Transaksi Petugas Lain', value: 'petugas_lain' },
]

// Data
const transactions = ref([])
const summary = ref({
  pemasukan: 0,
  pengeluaran: 0,
  saldo: 0,
  transaksi_saya: 0,
  pemasukan_saya: 0,
  total_transaksi: 0,
  transaksi_lunas: 0,
  transaksi_pending: 0,
})

// Get current user ID from localStorage
const currentUserId = computed(() => {
  return parseInt(localStorage.getItem('user_id')) || null
})

// Fetch data from API
const fetchRekap = async () => {
  loading.value = true
  try {
    // Fetch transactions for the selected date
    const response = await api.get('/api/petugas/transaksi', {
      params: {
        tanggal: selectedDate.value,
        jenis: filterType.value,
        filter_user: filterUser.value,
      },
    })

    if (response.data.success) {
      transactions.value = response.data.data || []
      // Gunakan summary dari API, bukan hitung manual
      if (response.data.summary) {
        summary.value = {
          ...summary.value,
          ...response.data.summary,
          saldo: response.data.summary.pemasukan - response.data.summary.pengeluaran,
        }
      }

      $q.notify({
        type: 'positive',
        message: 'Data berhasil dimuat',
        position: 'top',
        timeout: 1500,
      })
    } else {
      throw new Error(response.data.message || 'Gagal memuat data')
    }
  } catch (error) {
    console.error('Error fetching transactions:', error)
    transactions.value = []
    summary.value = {
      pemasukan: 0,
      pengeluaran: 0,
      saldo: 0,
      transaksi_saya: 0,
      pemasukan_saya: 0,
      total_transaksi: 0,
      transaksi_lunas: 0,
      transaksi_pending: 0,
    }
    $q.notify({
      type: 'negative',
      message: error.message || 'Gagal memuat data transaksi',
      position: 'top',
      timeout: 2000,
    })
  } finally {
    loading.value = false
  }
}

// Calculate summary statistics (backup calculation)

// Filter transactions based on selected filters
const filteredTransactions = computed(() => {
  let filtered = [...transactions.value]

  // Filter by type
  if (filterType.value !== 'semua') {
    filtered = filtered.filter((t) => t.jenis === filterType.value)
  }

  // Filter by user
  if (filterUser.value === 'saya') {
    filtered = filtered.filter((t) => t.petugas_id === currentUserId.value)
  } else if (filterUser.value === 'warga') {
    filtered = filtered.filter((t) => t.warga_id && !t.petugas_id)
  } else if (filterUser.value === 'petugas_lain') {
    filtered = filtered.filter((t) => t.petugas_id && t.petugas_id !== currentUserId.value)
  }

  return filtered.sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal))
})

// Table columns
const columns = [
  {
    name: 'kode',
    label: 'KODE / WAKTU',
    field: 'kode_transaksi',
    align: 'left',
    sortable: true,
  },
  {
    name: 'jenis',
    label: 'JENIS',
    field: 'jenis',
    align: 'center',
    sortable: true,
  },
  {
    name: 'user',
    label: 'USER',
    field: (row) => (row.warga_id ? 'warga' : 'petugas'),
    align: 'center',
    sortable: true,
  },
  {
    name: 'jumlah',
    label: 'JUMLAH',
    field: 'jumlah',
    align: 'right',
    sortable: true,
  },
  {
    name: 'status',
    label: 'STATUS',
    field: 'status_bayar',
    align: 'center',
    sortable: true,
  },
  {
    name: 'keterangan',
    label: 'KETERANGAN',
    field: 'keterangan',
    align: 'left',
  },
]

// Helper functions
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID').format(amount || 0)
}

const formatTime = (dateTime) => {
  if (!dateTime) return ''
  return date.formatDate(dateTime, 'HH:mm')
}

const getStatusColor = (status) => {
  switch (status) {
    case 'lunas':
      return 'green'
    case 'pending':
      return 'orange'
    case 'gagal':
      return 'red'
    default:
      return 'grey'
  }
}

// Watch for date changes
watch(selectedDateModel, () => {
  showDatePicker.value = false
  fetchRekap()
})

// Watch for filter changes
watch([filterType, filterUser], () => {
  fetchRekap()
})

// Initial fetch
onMounted(() => {
  fetchRekap()
})
</script>

<style scoped>
.q-page {
  background-color: #f1f8e9 !important;
}
.text-primary {
  color: #006837 !important;
}

.filter-card,
.date-card,
.summary-card,
.detail-card,
.stat-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.date-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.date-card:hover {
  background-color: #f5f5f5;
  transform: translateY(-2px);
}

.summary-card {
  padding: 16px;
}

.stat-card {
  padding: 8px;
}

.filter-select {
  border-radius: 8px;
}

.transaction-table :deep(.q-table__top) {
  padding: 0;
}

.transaction-table :deep(.q-table th) {
  font-weight: bold;
  background-color: #f8f9fa;
}

.transaction-table :deep(.q-table tbody tr:hover) {
  background-color: #f5f5f5;
}
</style>
