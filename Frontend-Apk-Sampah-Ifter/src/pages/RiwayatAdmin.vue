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
                  <div v-else class="text-grey-7">Admin</div>
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

    // Load aktivitas without params because backend returns all
    const res = await axios.get(`${API_URL}/api/riwayat_admin/`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (res.data.success) {
      let data = res.data.data

      // Frontend Filter Logic
      if (filterParams.value.jenis) {
         data = data.filter(d => d.type && d.type.toLowerCase() === filterParams.value.jenis.toLowerCase())
      }
      if (filterParams.value.kategori) {
         data = data.filter(d => d.type && d.type.toLowerCase() === filterParams.value.kategori.toLowerCase())
      }
      if (filterParams.value.start_date) {
         data = data.filter(d => new Date(d.tanggal) >= new Date(filterParams.value.start_date))
      }
      if (filterParams.value.end_date) {
         const end = new Date(filterParams.value.end_date)
         end.setHours(23, 59, 59, 999)
         data = data.filter(d => new Date(d.tanggal) <= end)
      }

      // Map Data for Table Display
      const mappedData = data.map(item => {
          let color = 'grey'
          let icon = 'info'
          let prefix = ''
          
          if (item.type === 'Pemasukan') {
             color = 'green'
             icon = 'arrow_downward'
             prefix = '+'
          } else if (item.type === 'Pengeluaran') {
             color = 'red'
             icon = 'arrow_upward'
             prefix = '-'
          } else if (item.type === 'Aktivitas') {
             color = 'blue'
             icon = 'local_shipping'
          }

          const dateObj = new Date(item.tanggal)
          const waktu = dateObj.toLocaleDateString('id-ID', {
            day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
          })
          
          let statusColor = 'orange'
          if (item.status === 'Completed' || item.status === 'Selesai') statusColor = 'green'
          else if (item.status === 'Batal') statusColor = 'red'
          
          return {
            ...item,
            waktu: waktu,
            color: color,
            icon: icon,
            jenis: item.type,
            kode_transaksi: item.type === 'Aktivitas' ? '-' : `TRX-${item.id}`,
            keterangan: item.description,
            kategori: item.type,
            jumlah_formatted: item.amount ? prefix + formatCurrency(item.amount) : '-',
            total_karung: item.jumlah_karung,
            status_color: statusColor,
            status_bayar: item.status,
            metode_bayar: item.type === 'Aktivitas' ? '' : 'Sistem'
          }
      })

      aktivitasList.value = mappedData

      // Calculate stats
      calculateStats(mappedData)
    }

    // Extract options
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
    if (item.type === 'Pemasukan') {
      pemasukan += parseFloat(item.amount || 0)
    } else if (item.type === 'Pengeluaran') {
      pengeluaran += parseFloat(item.amount || 0)
    }
  })

  stats.value.totalPemasukan = pemasukan
  stats.value.totalPengeluaran = pengeluaran
  stats.value.saldo = pemasukan - pengeluaran
  stats.value.totalAktivitas = data.length

  // Aggregation for chart (last 7 days)
  if (chartCanvas.value) {
    const today = new Date()
    const labels = []
    const pemasukanData = []
    const pengeluaranData = []

    for (let i = 6; i >= 0; i--) {
      const d = new Date(today)
      d.setDate(d.getDate() - i)
      const dateStr = d.toISOString().split('T')[0]
      labels.push(d.toLocaleDateString('id-ID', { day: 'numeric', month: 'short' }))

      const items = data.filter((item) => item.tanggal && item.tanggal.startsWith(dateStr))
      const sumMasuk = items
        .filter((item) => item.type === 'Pemasukan')
        .reduce((sum, item) => sum + parseFloat(item.amount || 0), 0)
      const sumKeluar = items
        .filter((item) => item.type === 'Pengeluaran')
        .reduce((sum, item) => sum + parseFloat(item.amount || 0), 0)

      pemasukanData.push(sumMasuk)
      pengeluaranData.push(sumKeluar)
    }

    renderChart({
      labels,
      datasets: [
        {
          label: 'Pemasukan',
          data: pemasukanData,
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Pengeluaran',
          data: pengeluaranData,
          borderColor: '#f44336',
          backgroundColor: 'rgba(244, 67, 54, 0.1)',
          fill: true,
          tension: 0.4
        },
      ],
    })
  }
}

const extractKategoriOptions = () => {
  const categories = new Set()
  aktivitasList.value.forEach((item) => {
    if (item.type) {
      categories.add(item.type)
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

const exportData = () => {
  exporting.value = true
  try {
    if (aktivitasList.value.length === 0) {
      $q.notify({ type: 'warning', message: 'Tidak ada data untuk diexport' })
      exporting.value = false
      return
    }

    const headers = ['Waktu', 'Jenis', 'Kode Transaksi', 'Keterangan', 'Petugas', 'Jumlah', 'Total Karung', 'Status', 'Metode Bayar']
    const rows = aktivitasList.value.map(item => [
      item.waktu ? item.waktu.replace(/,/g, '') : '',
      item.jenis || '',
      item.kode_transaksi || '',
      item.keterangan ? item.keterangan.replace(/,/g, ' ') : '-',
      item.nama_petugas ? item.nama_petugas.replace(/,/g, ' ') : 'Admin',
      item.amount || 0,
      item.total_karung || '-',
      item.status_bayar || '',
      item.metode_bayar || ''
    ])

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    
    link.setAttribute('href', url)
    link.setAttribute('download', 'laporan_aktivitas.csv')
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    $q.notify({ type: 'positive', message: 'Berhasil export data' })
  } catch (error) {
    console.error('Export error:', error)
    $q.notify({ type: 'negative', message: 'Gagal export data' })
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
