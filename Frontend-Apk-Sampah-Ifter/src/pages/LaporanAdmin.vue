<!-- src/pages/LaporanAdmin.vue -->
<template>
  <q-page class="q-pa-md">
    <div class="row items-center q-mb-lg">
      <q-btn
        flat
        round
        icon="arrow_back"
        color="primary"
        @click="$router.back()"
        class="bg-white shadow-1"
      />
      <div class="q-ml-md">
        <div class="text-h6 text-weight-bold text-primary">Laporan & Analisis</div>
        <div class="text-caption text-grey-7">Analisis data dan laporan operasional</div>
      </div>
    </div>

    <!-- Filter Laporan -->
    <q-card class="q-pa-md q-mb-lg">
      <div class="text-h6 text-weight-bold q-mb-md">Filter Laporan</div>
      <div class="row q-col-gutter-md">
        <div class="col-12 col-sm-6">
          <q-select filled v-model="filterJenis" :options="jenisLaporan" label="Jenis Laporan" />
        </div>
        <div class="col-12 col-sm-6">
          <q-select filled v-model="filterPeriode" :options="periodeLaporan" label="Periode" />
        </div>
        <div class="col-12 col-sm-6">
          <q-input filled v-model="filterTanggalMulai" label="Tanggal Mulai" type="date" />
        </div>
        <div class="col-12 col-sm-6">
          <q-input filled v-model="filterTanggalSelesai" label="Tanggal Selesai" type="date" />
        </div>
        <div class="col-12">
          <div class="row justify-end q-gutter-sm">
            <q-btn color="grey" label="Reset" @click="resetFilter" />
            <q-btn color="primary" label="Generate Laporan" @click="generateLaporan" />
            <q-btn color="green" icon="download" label="Export PDF" @click="exportPDF" />
          </div>
        </div>
      </div>
    </q-card>

    <!-- Statistik Laporan -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="q-pa-md text-center">
          <div class="text-h5 text-weight-bold text-primary">{{ statistik.totalTransaksi }}</div>
          <div class="text-caption">Total Transaksi</div>
        </q-card>
      </div>
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="q-pa-md text-center">
          <div class="text-h5 text-weight-bold text-green-9">
            {{ formatCurrency(statistik.totalPendapatan) }}
          </div>
          <div class="text-caption">Total Pendapatan</div>
        </q-card>
      </div>
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="q-pa-md text-center">
          <div class="text-h5 text-weight-bold text-blue-9">{{ statistik.totalPetugas }}</div>
          <div class="text-caption">Petugas Aktif</div>
        </q-card>
      </div>
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="q-pa-md text-center">
          <div class="text-h5 text-weight-bold text-orange-9">{{ statistik.laporanPending }}</div>
          <div class="text-caption">Laporan Pending</div>
        </q-card>
      </div>
    </div>

    <!-- Grafik Laporan -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-md-8">
        <q-card class="q-pa-md">
          <div class="text-h6 text-weight-bold q-mb-md">Trend Pendapatan Bulanan</div>
          <div class="chart-placeholder text-center q-pa-xl bg-grey-3 rounded-borders">
            <q-icon name="bar_chart" size="48px" color="grey-6" class="q-mb-sm" />
            <div class="text-grey-7">Grafik akan ditampilkan di sini</div>
          </div>
        </q-card>
      </div>
      <div class="col-12 col-md-4">
        <q-card class="q-pa-md">
          <div class="text-h6 text-weight-bold q-mb-md">Distribusi Layanan</div>
          <div class="chart-placeholder text-center q-pa-xl bg-grey-3 rounded-borders">
            <q-icon name="pie_chart" size="48px" color="grey-6" class="q-mb-sm" />
            <div class="text-grey-7">Diagram pie akan ditampilkan di sini</div>
          </div>
        </q-card>
      </div>
    </div>

    <!-- Tabel Laporan -->
    <q-card class="q-pa-md">
      <div class="row items-center justify-between q-mb-md">
        <div class="text-h6 text-weight-bold">Daftar Laporan</div>
        <div class="row items-center q-gutter-sm">
          <q-btn round flat icon="refresh" color="primary" @click="refreshData" />
          <q-btn color="primary" icon="add" label="Buat Laporan Baru" @click="buatLaporanBaru" />
        </div>
      </div>

      <q-table
        :rows="daftarLaporan"
        :columns="columnsLaporan"
        row-key="id"
        flat
        bordered
        :pagination="{ rowsPerPage: 10 }"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-badge
              :color="
                props.row.status === 'selesai'
                  ? 'green'
                  : props.row.status === 'proses'
                    ? 'orange'
                    : 'grey'
              "
              :label="props.row.status"
              rounded
            />
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props" align="center">
            <q-btn flat round dense icon="visibility" color="primary" size="sm" class="q-mr-xs" />
            <q-btn flat round dense icon="download" color="green" size="sm" />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Ringkasan -->
    <q-card class="q-pa-md q-mt-lg">
      <div class="text-h6 text-weight-bold q-mb-md">Ringkasan Analisis</div>
      <div class="row q-col-gutter-md">
        <div class="col-12 col-md-6">
          <div class="text-subtitle2 text-weight-bold q-mb-sm">📊 Insights</div>
          <ul class="q-pl-md">
            <li class="q-mb-xs">Pendapatan meningkat 15% dibanding bulan sebelumnya</li>
            <li class="q-mb-xs">Petugas paling produktif: Budi Santoso (45 transaksi)</li>
            <li class="q-mb-xs">Wilayah dengan layanan terbanyak: Blok A</li>
            <li>Rata-rata kepuasan pelanggan: 4.5/5</li>
          </ul>
        </div>
        <div class="col-12 col-md-6">
          <div class="text-subtitle2 text-weight-bold q-mb-sm">🎯 Rekomendasi</div>
          <ul class="q-pl-md">
            <li class="q-mb-xs">Tambah jadwal pengambilan di Blok C</li>
            <li class="q-mb-xs">Berikan reward untuk petugas berprestasi</li>
            <li class="q-mb-xs">Optimalkan rute pengambilan untuk efisiensi</li>
            <li>Perbaiki infrastruktur di zona dengan keluhan terbanyak</li>
          </ul>
        </div>
      </div>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Filter
const filterJenis = ref('semua')
const filterPeriode = ref('bulan_ini')
const filterTanggalMulai = ref('')
const filterTanggalSelesai = ref('')

const jenisLaporan = ['semua', 'keuangan', 'operasional', 'kinerja_petugas', 'kepuasan_pelanggan']

const periodeLaporan = ['hari_ini', 'minggu_ini', 'bulan_ini', 'tahun_ini', 'kustom']

// Statistik
const statistik = ref({
  totalTransaksi: 245,
  totalPendapatan: 18500000,
  totalPetugas: 15,
  laporanPending: 7,
})

// Data Laporan
const daftarLaporan = ref([
  {
    id: 1,
    nama: 'Laporan Keuangan Desember 2024',
    jenis: 'keuangan',
    periode: 'Desember 2024',
    dibuat: '2024-12-30',
    status: 'selesai',
  },
  {
    id: 2,
    nama: 'Laporan Kinerja Petugas Q4',
    jenis: 'kinerja_petugas',
    periode: 'Q4 2024',
    dibuat: '2024-12-28',
    status: 'selesai',
  },
  {
    id: 3,
    nama: 'Laporan Operasional Harian',
    jenis: 'operasional',
    periode: '30 Des 2024',
    dibuat: '2024-12-30',
    status: 'proses',
  },
  {
    id: 4,
    nama: 'Analisis Kepuasan Pelanggan',
    jenis: 'kepuasan_pelanggan',
    periode: 'November 2024',
    dibuat: '2024-11-30',
    status: 'selesai',
  },
])

const columnsLaporan = [
  { name: 'nama', label: 'Nama Laporan', field: 'nama', align: 'left' },
  { name: 'jenis', label: 'Jenis', field: 'jenis', align: 'left' },
  { name: 'periode', label: 'Periode', field: 'periode', align: 'left' },
  { name: 'dibuat', label: 'Dibuat', field: 'dibuat', align: 'left' },
  { name: 'status', label: 'Status', field: 'status', align: 'center' },
  { name: 'actions', label: 'Aksi', align: 'center' },
]

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
  }).format(amount)
}

const resetFilter = () => {
  filterJenis.value = 'semua'
  filterPeriode.value = 'bulan_ini'
  filterTanggalMulai.value = ''
  filterTanggalSelesai.value = ''
}

const generateLaporan = () => {
  $q.loading.show({ message: 'Membuat laporan...' })
  setTimeout(() => {
    $q.loading.hide()
    $q.notify({
      type: 'positive',
      message: 'Laporan berhasil dibuat',
      position: 'top',
      timeout: 2000,
    })
  }, 1500)
}

const exportPDF = () => {
  $q.notify({
    type: 'info',
    message: 'Fitur export PDF akan segera tersedia',
    position: 'top',
    timeout: 2000,
  })
}

const refreshData = () => {
  $q.notify({
    type: 'info',
    message: 'Memperbarui data...',
    position: 'top',
    timeout: 1000,
  })
}

const buatLaporanBaru = () => {
  $q.dialog({
    title: 'Buat Laporan Baru',
    message: 'Pilih jenis laporan yang ingin dibuat:',
    options: {
      type: 'radio',
      model: 'keuangan',
      items: [
        { label: 'Laporan Keuangan', value: 'keuangan' },
        { label: 'Laporan Operasional', value: 'operasional' },
        { label: 'Laporan Kinerja Petugas', value: 'kinerja_petugas' },
        { label: 'Laporan Kepuasan Pelanggan', value: 'kepuasan_pelanggan' },
      ],
    },
    cancel: true,
    persistent: true,
  }).onOk((data) => {
    $q.notify({
      type: 'info',
      message: `Membuat laporan ${data}`,
      position: 'top',
      timeout: 2000,
    })
  })
}
</script>

<style scoped>
.chart-placeholder {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
