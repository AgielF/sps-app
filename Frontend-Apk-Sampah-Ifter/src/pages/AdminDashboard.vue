<template>
  <q-page class="q-pa-md bg-grey-1">
    <!-- Header dengan Welcome & Date -->
    <div class="row items-center q-mb-lg">
      <div class="col">
        <div class="text-h4 text-weight-bold text-primary">Dashboard Admin</div>
        <div class="text-subtitle1 text-grey-7">{{ welcomeMessage }} • {{ currentDate }}</div>
      </div>
      <div class="col-auto">
        <q-btn color="primary" icon="refresh" round @click="refreshDashboard" :loading="loading">
          <q-tooltip>Refresh Dashboard</q-tooltip>
        </q-btn>
      </div>
    </div>

    <!-- QUICK STATS CARDS -->
    <div class="row q-col-gutter-md q-mb-lg">
      <!-- Today's Revenue -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-blue-grey-1">
          <q-card-section class="text-center">
            <div class="text-h6 text-weight-bold text-blue-grey-10">
              {{ formatCurrency(stats.today?.total || 0) }}
            </div>
            <div class="text-caption text-blue-grey-8">Hari Ini</div>
            <div class="text-caption text-blue-grey-6">
              {{ stats.today?.transaksi || 0 }} transaksi
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Monthly Revenue -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-cyan-1">
          <q-card-section class="text-center">
            <div class="text-h6 text-weight-bold text-cyan-10">
              {{ formatCurrency(stats.month?.total || 0) }}
            </div>
            <div class="text-caption text-cyan-8">Bulan Ini</div>
            <div class="text-caption text-cyan-6">{{ stats.month?.transaksi || 0 }} transaksi</div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Active Petugas -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-green-1">
          <q-card-section class="text-center">
            <div class="text-h6 text-weight-bold text-green-10">
              {{ stats.active_petugas?.count || 0 }}
            </div>
            <div class="text-caption text-green-8">Petugas Aktif</div>
            <div class="text-caption text-green-6">
              {{ stats.petugas_stats?.total_petugas || 0 }} total
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Today's Schedule -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-orange-1">
          <q-card-section class="text-center">
            <div class="text-h6 text-weight-bold text-orange-10">
              {{ stats.today_schedule_count?.count || 0 }}
            </div>
            <div class="text-caption text-orange-8">Jadwal Hari Ini</div>
            <q-btn
              v-if="stats.today_schedule_count?.count > 0"
              label="Lihat"
              color="orange"
              flat
              dense
              @click="viewSchedule"
              class="q-mt-xs"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- MAIN CONTENT ROW -->
    <div class="row q-col-gutter-lg">
      <!-- LEFT COLUMN: Charts -->
      <div class="col-12 col-lg-8">
        <!-- Revenue Chart -->
        <q-card class="q-mb-lg shadow-1">
          <q-card-section>
            <div class="row items-center">
              <div class="col">
                <div class="text-h6">Trend 7 Hari Terakhir</div>
                <div class="text-caption text-grey-6">Pemasukan vs Pengeluaran</div>
              </div>
              <div class="col-auto">
                <q-btn-toggle
                  v-model="chartPeriod"
                  :options="chartPeriodOptions"
                  spread
                  dense
                  color="primary"
                  flat
                />
              </div>
            </div>
          </q-card-section>
          <q-card-section style="height: 300px">
            <canvas ref="revenueChart"></canvas>
          </q-card-section>
        </q-card>

        <!-- Transaction Stats -->
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <q-card class="shadow-1">
              <q-card-section>
                <div class="text-h6 q-mb-md">Statistik Transaksi</div>
                <div class="q-gutter-y-md">
                  <div v-for="type in transactionTypes" :key="type.jenis" class="row items-center">
                    <div class="col">
                      <div class="text-weight-medium">{{ getTypeLabel(type.jenis) }}</div>
                      <div class="text-caption text-grey-6">{{ type.count }} transaksi</div>
                    </div>
                    <div class="col-auto">
                      <div class="text-h6" :class="getAmountColor(type.jenis)">
                        {{ formatCurrency(type.total) }}
                      </div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6">
            <q-card class="shadow-1">
              <q-card-section>
                <div class="text-h6 q-mb-md">Ringkasan Bulanan</div>
                <div class="q-gutter-y-md">
                  <div class="row items-center">
                    <div class="col">
                      <div class="text-weight-medium">Pemasukan</div>
                      <div class="text-caption text-grey-6">Bulan {{ currentMonth }}</div>
                    </div>
                    <div class="col-auto">
                      <div class="text-h6 text-green">
                        {{ formatCurrency(dashboardData.monthly_stats?.pemasukan_bulan_ini || 0) }}
                      </div>
                    </div>
                  </div>
                  <div class="row items-center">
                    <div class="col">
                      <div class="text-weight-medium">Pengeluaran</div>
                      <div class="text-caption text-grey-6">Termasuk gaji</div>
                    </div>
                    <div class="col-auto">
                      <div class="text-h6 text-red">
                        {{
                          formatCurrency(dashboardData.monthly_stats?.pengeluaran_bulan_ini || 0)
                        }}
                      </div>
                    </div>
                  </div>
                  <div class="row items-center">
                    <div class="col">
                      <div class="text-weight-bold">Saldo Bulan Ini</div>
                    </div>
                    <div class="col-auto">
                      <div class="text-h5" :class="saldoClass">
                        {{ formatCurrency(dashboardData.monthly_stats?.saldo_bulan_ini || 0) }}
                      </div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN: Sidebar -->
      <div class="col-12 col-lg-4">
        <!-- Today's Schedule -->
        <q-card class="q-mb-lg shadow-1">
          <q-card-section>
            <div class="text-h6">Jadwal Hari Ini</div>
            <div class="text-caption text-grey-6">{{ currentDate }}</div>
          </q-card-section>

          <q-card-section v-if="loading" class="text-center">
            <q-spinner size="sm" />
          </q-card-section>

          <q-card-section v-else-if="!todaySchedule.length" class="text-center text-grey-6">
            <q-icon name="event_available" size="2em" class="q-mb-sm" />
            <div>Tidak ada jadwal hari ini</div>
          </q-card-section>

          <q-list v-else bordered>
            <q-item v-for="schedule in todaySchedule" :key="schedule.id" class="q-py-sm">
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ schedule.wilayah }}</q-item-label>
                <q-item-label caption>
                  {{ schedule.jam_mulai }} - {{ schedule.jam_selesai }}
                </q-item-label>
                <q-item-label v-if="schedule.keterangan" caption class="text-grey-6">
                  {{ schedule.keterangan }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn icon="visibility" flat round dense @click="viewScheduleDetail(schedule)" />
              </q-item-section>
            </q-item>
          </q-list>

          <q-card-actions align="right">
            <q-btn label="Lihat Semua Jadwal" color="primary" flat to="/admin/jadwal/list" />
          </q-card-actions>
        </q-card>

        <!-- Recent Transactions -->
        <q-card class="shadow-1">
          <q-card-section>
            <div class="text-h6">Transaksi Terbaru</div>
            <div class="text-caption text-grey-6">8 transaksi terakhir</div>
          </q-card-section>

          <q-card-section v-if="loading" class="text-center">
            <q-spinner size="sm" />
          </q-card-section>

          <q-card-section v-else-if="!recentTransactions.length" class="text-center text-grey-6">
            <q-icon name="receipt_long" size="2em" class="q-mb-sm" />
            <div>Belum ada transaksi</div>
          </q-card-section>

          <q-list v-else bordered>
            <q-item v-for="transaction in recentTransactions" :key="transaction.id" class="q-py-xs">
              <q-item-section avatar>
                <q-icon
                  :name="getTransactionIcon(transaction.jenis)"
                  :color="getTransactionColor(transaction.jenis)"
                />
              </q-item-section>

              <q-item-section>
                <q-item-label class="text-weight-medium">
                  {{
                    transaction.keterangan?.substring(0, 30) || transaction.kategori || 'Transaksi'
                  }}
                </q-item-label>
                <q-item-label caption>
                  {{ transaction.waktu }} • {{ transaction.petugas || '-' }}
                </q-item-label>
              </q-item-section>

              <q-item-section side>
                <div :class="`text-weight-bold text-${getTransactionColor(transaction.jenis)}`">
                  {{ formatCurrency(transaction.jumlah) }}
                </div>
              </q-item-section>
            </q-item>
          </q-list>

          <q-card-actions align="right">
            <q-btn label="Lihat Semua Transaksi" color="primary" flat to="/log-aktivitas" />
          </q-card-actions>
        </q-card>

        <!-- Quick Actions -->
        <q-card class="q-mt-lg shadow-1">
          <q-card-section>
            <div class="text-h6 q-mb-md">Aksi Cepat</div>
            <div class="row q-col-gutter-sm">
              <div class="col-6">
                <q-btn
                  color="primary"
                  icon="add"
                  label="Tambah Transaksi"
                  class="full-width"
                  to="/admin/keuangan"
                />
              </div>
              <div class="col-6">
                <q-btn
                  color="green"
                  icon="paid"
                  label="Input Gaji"
                  class="full-width"
                  to="/admin/gaji"
                />
              </div>
              <div class="col-6">
                <q-btn
                  color="orange"
                  icon="event"
                  label="Buat Jadwal"
                  class="full-width"
                  to="/admin/jadwal/tambah"
                />
              </div>
              <div class="col-6">
                <q-btn
                  color="blue"
                  icon="download"
                  label="Export Laporan"
                  class="full-width"
                  @click="exportReport"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- BOTTOM SECTION: Top Petugas -->
    <div class="row q-mt-lg">
      <div class="col-12">
        <q-card class="shadow-1">
          <q-card-section>
            <div class="text-h6">Top 5 Petugas</div>
            <div class="text-caption text-grey-6">Berdasarkan total transaksi</div>
          </q-card-section>

          <q-card-section v-if="loading" class="text-center">
            <q-spinner size="sm" />
          </q-card-section>

          <q-card-section v-else-if="!topPetugas.length" class="text-center text-grey-6">
            <q-icon name="people" size="2em" class="q-mb-sm" />
            <div>Belum ada data petugas</div>
          </q-card-section>

          <div v-else class="row q-col-gutter-md">
            <div
              v-for="petugas in topPetugas"
              :key="petugas.nama_lengkap"
              class="col-12 col-sm-6 col-md-4 col-lg"
            >
              <q-card flat bordered class="text-center">
                <q-card-section>
                  <q-avatar size="60px" color="primary" text-color="white" class="q-mb-sm">
                    {{ getInitials(petugas.nama_lengkap) }}
                  </q-avatar>
                  <div class="text-weight-bold">{{ petugas.nama_lengkap }}</div>
                  <div class="text-caption text-grey-7">{{ petugas.no_telepon }}</div>
                  <div class="text-h6 text-primary q-mt-sm">
                    {{ formatCurrency(petugas.total_transaksi || 0) }}
                  </div>
                  <div class="text-caption">{{ petugas.jumlah_transaksi || 0 }} transaksi</div>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const $q = useQuasar()
const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

// Refs
const loading = ref(false)
const revenueChart = ref(null)
let chartInstance = null

// Data
const stats = ref({})
const dashboardData = ref({})
const chartPeriod = ref('7days')

// Chart options
const chartPeriodOptions = [
  { label: '7 Hari', value: '7days' },
  { label: '30 Hari', value: '30days' },
  { label: 'Bulan Ini', value: 'month' },
]

// Computed
const welcomeMessage = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Selamat Pagi!'
  if (hour < 18) return 'Selamat Siang!'
  return 'Selamat Malam!'
})

const currentDate = computed(() => {
  return new Date().toLocaleDateString('id-ID', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
})

const currentMonth = computed(() => {
  return new Date().toLocaleDateString('id-ID', { month: 'long' })
})

const todaySchedule = computed(() => {
  return dashboardData.value.today_schedule || []
})

const recentTransactions = computed(() => {
  return dashboardData.value.recent_transactions || []
})

const topPetugas = computed(() => {
  return dashboardData.value.top_petugas || []
})

const transactionTypes = computed(() => {
  return dashboardData.value.transaction_by_type || []
})

const saldoClass = computed(() => {
  const saldo = dashboardData.value.monthly_stats?.saldo_bulan_ini || 0
  return saldo >= 0 ? 'text-green' : 'text-red'
})

// Helper Functions
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
  }).format(amount || 0)
}

const getInitials = (name) => {
  if (!name) return '?'
  return name
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

const getTransactionIcon = (jenis) => {
  const icons = {
    pemasukan: 'arrow_upward',
    pengeluaran: 'arrow_downward',
    gaji: 'paid',
    topup: 'account_balance_wallet',
  }
  return icons[jenis] || 'receipt'
}

const getTransactionColor = (jenis) => {
  const colors = {
    pemasukan: 'green',
    pengeluaran: 'red',
    gaji: 'orange',
    topup: 'blue',
  }
  return colors[jenis] || 'grey'
}

const getTypeLabel = (jenis) => {
  const labels = {
    pemasukan: 'Pemasukan',
    pengeluaran: 'Pengeluaran',
    gaji: 'Gaji Petugas',
    topup: 'Topup Saldo',
  }
  return labels[jenis] || jenis
}

const getAmountColor = (jenis) => {
  return jenis === 'pemasukan' ? 'text-green' : 'text-red'
}

// Methods
const loadDashboard = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')

    // Load quick stats
    const statsRes = await axios.get(`${API_URL}/api/dashboard/quick-stats`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (statsRes.data.success) {
      stats.value = statsRes.data.data
    }

    // Load full dashboard data
    const dashboardRes = await axios.get(`${API_URL}/api/dashboard/summary`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (dashboardRes.data.success) {
      dashboardData.value = dashboardRes.data.data
      renderChart()
    }
  } catch (error) {
    console.error('Error loading dashboard:', error)
    $q.notify({
      type: 'negative',
      message: 'Gagal memuat dashboard',
      caption: error.message,
    })
  } finally {
    loading.value = false
  }
}

const renderChart = () => {
  if (!dashboardData.value.chart_data) return

  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy()
  }

  nextTick(() => {
    if (!revenueChart.value) return

    const ctx = revenueChart.value.getContext('2d')
    const chartData = dashboardData.value.chart_data

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: 'Pemasukan',
            data: chartData.pemasukan,
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
          },
          {
            label: 'Pengeluaran',
            data: chartData.pengeluaran,
            borderColor: '#F44336',
            backgroundColor: 'rgba(244, 67, 54, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              padding: 20,
              usePointStyle: true,
            },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${formatCurrency(context.raw)}`
              },
            },
          },
        },
        scales: {
          x: {
            grid: {
              display: false,
            },
          },
          y: {
            beginAtZero: true,
            ticks: {
              callback: (value) => formatCurrency(value).replace('Rp', ''),
            },
            grid: {
              color: 'rgba(0,0,0,0.05)',
            },
          },
        },
        interaction: {
          intersect: false,
          mode: 'nearest',
        },
      },
    })
  })
}

const refreshDashboard = () => {
  loadDashboard()
  $q.notify({
    type: 'info',
    message: 'Memperbarui dashboard...',
    timeout: 1000,
  })
}

const viewSchedule = () => {
  router.push('')
}

const viewScheduleDetail = (schedule) => {
  // Implement detail view
  $q.notify({
    message: `Detail jadwal: ${schedule.wilayah}`,
    caption: `${schedule.jam_mulai} - ${schedule.jam_selesai}`,
    color: 'info',
  })
}

const exportReport = () => {
  $q.notify({
    message: 'Mengekspor laporan...',
    color: 'info',
    icon: 'download',
  })
  // Implement export logic
  window.open(`${API_URL}/api/log/export-csv`, '_blank')
}

// Auto-refresh every 60 seconds
let refreshInterval
const startAutoRefresh = () => {
  refreshInterval = setInterval(() => {
    if (!loading.value) {
      loadDashboard()
    }
  }, 60000)
}

// Lifecycle
onMounted(() => {
  loadDashboard()
  startAutoRefresh()
})

// Cleanup
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

<style scoped>
/* Custom styles */
.q-card {
  border-radius: 12px;
  transition: transform 0.2s ease-in-out;
}

.q-card:hover {
  transform: translateY(-2px);
}

.q-list--bordered {
  border-radius: 8px;
}

.text-shadow {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .text-h4 {
    font-size: 1.5rem;
  }

  .q-card-section {
    padding: 12px;
  }
}
</style>
