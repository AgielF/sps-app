<template>
  <q-page class="q-pa-md bg-grey-1">
    <!-- Header -->
    <div class="row items-center q-mb-md">
      <div class="col">
        <div class="text-h5 text-weight-bold">Log Aktivitas</div>
        <div class="text-caption text-grey-7">Rekap semua transaksi dan pengambilan</div>
      </div>
      <div class="col-auto">
        <q-btn label="Export" color="primary" icon="download" @click="exportData" />
      </div>
    </div>

    <!-- Filter Section -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-3">
            <q-select
              v-model="filter.jenis"
              :options="jenisOptions"
              label="Jenis Transaksi"
              outlined
              clearable
              dense
            />
          </div>
          <div class="col-12 col-md-3">
            <q-select
              v-model="filter.kategori"
              :options="kategoriOptions"
              label="Kategori"
              outlined
              clearable
              dense
            />
          </div>
          <div class="col-12 col-md-3">
            <q-input
              v-model="filter.startDate"
              label="Dari Tanggal"
              type="date"
              outlined
              dense
              clearable
            />
          </div>
          <div class="col-12 col-md-3">
            <q-input
              v-model="filter.endDate"
              label="Sampai Tanggal"
              type="date"
              outlined
              dense
              clearable
            />
          </div>
        </div>
        <div class="row q-mt-sm">
          <div class="col">
            <q-btn label="Terapkan Filter" color="primary" @click="loadAktivitas" />
            <q-btn label="Reset" flat @click="resetFilter" class="q-ml-sm" />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Stats Cards -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-3">
        <q-card class="bg-blue-1">
          <q-card-section>
            <div class="text-h6">{{ formatCurrency(stats.totalPemasukan) }}</div>
            <div class="text-caption">Total Pemasukan</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card class="bg-red-1">
          <q-card-section>
            <div class="text-h6">{{ formatCurrency(stats.totalPengeluaran) }}</div>
            <div class="text-caption">Total Pengeluaran</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card class="bg-green-1">
          <q-card-section>
            <div class="text-h6">{{ stats.totalAktivitas }}</div>
            <div class="text-caption">Total Aktivitas</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card class="bg-orange-1">
          <q-card-section>
            <div class="text-h6">{{ formatCurrency(stats.saldo) }}</div>
            <div class="text-caption">Saldo</div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Chart (7 hari terakhir) -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6 q-mb-md">Trend 7 Hari Terakhir</div>
        <div style="height: 300px">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </q-card-section>
    </q-card>

    <!-- Activity Table -->
    <q-card>
      <q-card-section>
        <div class="row items-center q-mb-md">
          <div class="col">
            <div class="text-h6">Daftar Aktivitas</div>
          </div>
          <div class="col-auto">
            <q-btn
              label="Refresh"
              icon="refresh"
              color="secondary"
              @click="loadAktivitas"
              :loading="loading"
            />
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center q-py-lg">
          <q-spinner color="primary" size="2em" />
          <div class="text-caption q-mt-sm">Memuat data aktivitas...</div>
        </div>

        <!-- No Data -->
        <div v-else-if="aktivitasList.length === 0" class="text-center q-py-lg text-grey-7">
          <q-icon name="receipt_long" size="4em" class="q-mb-sm" />
          <div>Tidak ada data aktivitas</div>
        </div>

        <!-- Activity List -->
        <div v-else>
          <q-table
            :rows="aktivitasList"
            :columns="columns"
            row-key="id"
            flat
            bordered
            :pagination="pagination"
          >
            <!-- Custom Body -->
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="waktu" :props="props">
                  <div class="text-weight-medium">{{ props.row.waktu }}</div>
                </q-td>

                <q-td key="jenis" :props="props">
                  <q-badge :color="props.row.color">
                    <q-icon :name="props.row.icon" size="xs" class="q-mr-xs" />
                    {{ props.row.jenis }}
                  </q-badge>
                </q-td>

                <q-td key="kode" :props="props">
                  <div>{{ props.row.kode_transaksi || '-' }}</div>
                  <div class="text-caption text-grey-7">#{{ props.row.id }}</div>
                </q-td>

                <q-td key="keterangan" :props="props">
                  <div>{{ props.row.keterangan || '-' }}</div>
                  <div v-if="props.row.kategori" class="text-caption text-grey-7">
                    {{ props.row.kategori }}
                  </div>
                </q-td>

                <q-td key="petugas" :props="props">
                  <div v-if="props.row.nama_petugas">
                    {{ props.row.nama_petugas }}
                    <div class="text-caption text-grey-7">
                      {{ props.row.telepon_petugas || '' }}
                    </div>
                  </div>
                  <div v-else class="text-grey-7">-</div>
                </q-td>

                <q-td key="jumlah" :props="props">
                  <div class="text-weight-bold" :class="`text-${props.row.color}`">
                    {{ props.row.jumlah_formatted }}
                  </div>
                  <div v-if="props.row.total_karung" class="text-caption">
                    {{ props.row.total_karung }} karung
                  </div>
                </q-td>

                <q-td key="status" :props="props">
                  <q-badge :color="props.row.status_color">
                    {{ props.row.status_bayar || 'pending' }}
                  </q-badge>
                  <div class="text-caption q-mt-xs">
                    {{ props.row.metode_bayar || 'cash' }}
                  </div>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useQuasar } from 'quasar'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const $q = useQuasar()
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

// Refs
const loading = ref(false)
const loadingChart = ref(false)
const aktivitasList = ref([])
const chartCanvas = ref(null)
let chartInstance = null

const exporting = ref(false)

// Filter
const filter = ref({
  jenis: null,
  kategori: null,
  startDate: null,
  endDate: null,
})

// Stats
const stats = ref({
  totalPemasukan: 0,
  totalPengeluaran: 0,
  totalAktivitas: 0,
  saldo: 0,
})

// Options
const jenisOptions = [
  { label: 'Pemasukan', value: 'pemasukan' },
  { label: 'Pengeluaran', value: 'pengeluaran' },
  { label: 'Gaji', value: 'gaji' },
  { label: 'Topup', value: 'topup' },
]

const kategoriOptions = ref([])

// Table Columns
const columns = [
  { name: 'waktu', label: 'Waktu', align: 'left', field: 'waktu', sortable: true },
  { name: 'jenis', label: 'Jenis', align: 'center', field: 'jenis' },
  { name: 'kode', label: 'Kode Transaksi', align: 'left', field: 'kode_transaksi' },
  { name: 'keterangan', label: 'Keterangan', align: 'left', field: 'keterangan' },
  { name: 'petugas', label: 'Petugas', align: 'left', field: 'nama_petugas' },
  { name: 'jumlah', label: 'Jumlah', align: 'right', field: 'jumlah', sortable: true },
  { name: 'status', label: 'Status', align: 'center', field: 'status_bayar' },
]

const pagination = {
  rowsPerPage: 20,
}

// Computed
const filterParams = computed(() => {
  const params = {}
  if (filter.value.jenis) params.jenis = filter.value.jenis.value || filter.value.jenis
  if (filter.value.kategori) params.kategori = filter.value.kategori.value || filter.value.kategori
  if (filter.value.startDate) params.start_date = filter.value.startDate
  if (filter.value.endDate) params.end_date = filter.value.endDate
  return params
})

// Helper Functions
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
  }).format(amount || 0)
}

// Methods
const loadAktivitas = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')

    // Load aktivitas
    const res = await axios.get(`${API_URL}/api/log/aktivitas`, {
      headers: { Authorization: `Bearer ${token}` },
      params: filterParams.value,
    })

    if (res.data.success) {
      aktivitasList.value = res.data.data

      // Calculate stats
      calculateStats(res.data.data)
    }

    // Load summary
    await loadSummary()

    // Load chart
    await loadChart()

    // Load kategori options dari data
    extractKategoriOptions()
  } catch (error) {
    console.error('Error loading aktivitas:', error)
    $q.notify({
      type: 'negative',
      message: 'Gagal memuat data aktivitas',
      caption: error.message,
    })
  } finally {
    loading.value = false
  }
}

const loadSummary = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${API_URL}/api/log/summary`, {
      headers: { Authorization: `Bearer ${token}` },
      params: filterParams.value,
    })

    if (res.data.success) {
      const data = res.data.data
      if (data.totals) {
        stats.value.totalAktivitas = data.totals.total_aktivitas || 0
        stats.value.totalPemasukan = data.totals.total_pemasukan || 0
        stats.value.totalPengeluaran = data.totals.total_pengeluaran || 0
        stats.value.saldo =
          (data.totals.total_pemasukan || 0) - (data.totals.total_pengeluaran || 0)
      }
    }
  } catch (error) {
    console.error('Error loading summary:', error)
  }
}

const loadChart = async () => {
  loadingChart.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${API_URL}/api/log/harian`, {
      headers: { Authorization: `Bearer ${token}` },
      params: { days: 7 },
    })

    if (res.data.success && chartCanvas.value) {
      renderChart(res.data.data)
    }
  } catch (error) {
    console.error('Error loading chart:', error)
  } finally {
    loadingChart.value = false
  }
}

const renderChart = (chartData) => {
  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.labels,
      datasets: chartData.datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              return `${context.dataset.label}: ${formatCurrency(context.raw)}`
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => formatCurrency(value),
          },
        },
      },
    },
  })
}

const calculateStats = (data) => {
  let pemasukan = 0
  let pengeluaran = 0

  data.forEach((item) => {
    if (item.jenis === 'pemasukan') {
      pemasukan += parseFloat(item.jumlah)
    } else if (['pengeluaran', 'gaji'].includes(item.jenis)) {
      pengeluaran += parseFloat(item.jumlah)
    }
  })

  stats.value.totalPemasukan = pemasukan
  stats.value.totalPengeluaran = pengeluaran
  stats.value.saldo = pemasukan - pengeluaran
  stats.value.totalAktivitas = data.length
}

const extractKategoriOptions = () => {
  const categories = new Set()
  aktivitasList.value.forEach((item) => {
    if (item.kategori) {
      categories.add(item.kategori)
    }
  })

  kategoriOptions.value = Array.from(categories).map((cat) => ({
    label: cat,
    value: cat,
  }))
}

const resetFilter = () => {
  filter.value = {
    jenis: null,
    kategori: null,
    startDate: null,
    endDate: null,
  }
  loadAktivitas()
}

const exportData = async () => {
  exporting.value = true
  try {
    const token = localStorage.getItem('token')

    // Build query params
    const params = new URLSearchParams()
    if (filter.value.startDate) params.append('start_date', filter.value.startDate)
    if (filter.value.endDate) params.append('end_date', filter.value.endDate)
    if (filter.value.jenis) params.append('jenis', filter.value.jenis.value || filter.value.jenis)
    if (filter.value.kategori)
      params.append('kategori', filter.value.kategori.value || filter.value.kategori)

    const url = `${API_URL}/api/log/export-csv?${params.toString()}`

    // Fetch dengan headers
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    // Get filename from Content-Disposition header
    const contentDisposition = response.headers.get('content-disposition')
    let filename = 'laporan_transaksi.csv'

    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1].replace(/['"]/g, '')
      }
    }

    // Convert to blob and download
    const blob = await response.blob()
    const blobUrl = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = blobUrl
    link.download = filename
    link.style.display = 'none'

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    // Cleanup
    window.URL.revokeObjectURL(blobUrl)

    $q.notify({
      type: 'positive',
      message: `File "${filename}" berhasil didownload`,
      timeout: 3000,
    })
  } catch (error) {
    console.error('Export error:', error)
    $q.notify({
      type: 'negative',
      message: 'Gagal export data',
      caption: error.message,
    })
  } finally {
    exporting.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadAktivitas()
})

// Watch for filter changes
watch(
  filterParams,
  () => {
    // Auto reload when filter changes (optional)
    // loadAktivitas()
  },
  { deep: true },
)
</script>

<style scoped>
.q-table th {
  font-weight: bold;
  background-color: #f5f5f5;
}
</style>
