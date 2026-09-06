<template>
  <q-page class="q-pa-md bg-green-1">
    <!-- Header -->
    <div class="row items-center q-mb-md">
      <div class="col">
        <div class="text-h6 text-weight-bold text-dark">Jadwal Pengambilan Sampah</div>
        <div class="text-caption text-grey-7">Kelola jadwal pengambilan sampah</div>
      </div>
      <div class="col-auto">
        <q-btn
          label="Tambah Jadwal"
          color="primary"
          icon="add"
          :to="{ name: 'TambahJadwal' }"
          class="q-px-md"
        />
        <q-btn icon="refresh" color="grey" flat round @click="loadJadwal" />
      </div>
    </div>

    <!-- Filter -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-3">
        <q-input
          v-model="filter.tanggal"
          label="Filter Tanggal"
          outlined
          dense
          type="date"
          clearable
        />
      </div>
      <div class="col-12 col-md-3">
        <q-select
          v-model="filter.status"
          label="Filter Status"
          outlined
          dense
          :options="statusOptions"
          clearable
          emit-value
          map-options
        />
      </div>
      <div class="col-12 col-md-6">
        <q-input v-model="filter.search" label="Cari Wilayah" outlined dense clearable>
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center q-py-lg">
      <q-spinner color="primary" size="2em" />
      <div class="text-grey-7 q-mt-sm">Memuat data jadwal...</div>
    </div>

    <!-- Jadwal List -->
    <div v-else>
      <!-- Stats Cards -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-6 col-sm-3">
          <q-card class="stat-card text-center">
            <q-card-section>
              <div class="text-h6 text-primary">{{ jadwalList.length }}</div>
              <div class="text-caption text-grey-7">Total Jadwal</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6 col-sm-3">
          <q-card class="stat-card text-center">
            <q-card-section>
              <div class="text-h6 text-green">{{ activeSchedules }}</div>
              <div class="text-caption text-grey-7">Aktif</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6 col-sm-3">
          <q-card class="stat-card text-center">
            <q-card-section>
              <div class="text-h6 text-orange">{{ todaySchedules }}</div>
              <div class="text-caption text-grey-7">Hari Ini</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6 col-sm-3">
          <q-card class="stat-card text-center">
            <q-card-section>
              <div class="text-h6 text-blue">{{ upcomingSchedules }}</div>
              <div class="text-caption text-grey-7">Mendatang</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Table -->
      <q-card class="data-card">
        <q-table
          :rows="filteredJadwal"
          :columns="columns"
          row-key="id"
          flat
          bordered
          :pagination="{ rowsPerPage: 10 }"
          :loading="loading"
        >
          <!-- Tanggal Column -->
          <template v-slot:body-cell-tanggal="props">
            <q-td :props="props">
              <div class="column">
                <div class="text-weight-medium">
                  {{ formatDate(props.row.tanggal) }}
                </div>
                <div class="text-caption text-grey-7">
                  {{ getDayName(props.row.tanggal) }}
                </div>
              </div>
            </q-td>
          </template>

          <!-- Jam Column -->
          <template v-slot:body-cell-jam="props">
            <q-td :props="props">
              <div class="column">
                <div class="row items-center">
                  <q-icon name="schedule" size="14px" class="q-mr-xs text-green-7" />
                  <span class="text-weight-medium">{{ formatTime(props.row.jam_mulai) }}</span>
                  <span class="q-mx-xs text-grey-5">-</span>
                  <span class="text-weight-medium">{{ formatTime(props.row.jam_selesai) }}</span>
                </div>
                <div class="text-caption text-grey-7">
                  Durasi: {{ calculateDuration(props.row.jam_mulai, props.row.jam_selesai) }}
                </div>
              </div>
            </q-td>
          </template>

          <!-- Wilayah Column -->
          <!-- Di dalam template, update kolom wilayah menjadi: -->
          <!-- Ganti bagian template untuk menampilkan petugas: -->
          <!-- Di template slot wilayah -->
          <template v-slot:body-cell-wilayah="props">
            <q-td :props="props">
              <div class="text-body2" style="max-width: 300px; white-space: normal">
                <div class="text-weight-medium">{{ props.row.wilayah || '-' }}</div>

                <!-- Tampilkan petugas dari string gabungan -->
                <div v-if="props.row.nama_petugas" class="q-mt-xs">
                  <div class="text-caption text-grey-7">Petugas:</div>
                  <div class="q-mt-xs">
                    <template
                      v-for="(petugas, index) in getPetugasList(props.row.nama_petugas)"
                      :key="index"
                    >
                      <q-chip size="xs" color="blue" text-color="white" class="q-mr-xs q-mb-xs">
                        {{ petugas }}
                      </q-chip>
                    </template>
                  </div>
                </div>

                <div v-if="props.row.keterangan" class="text-caption text-grey-7 q-mt-xs">
                  {{ props.row.keterangan }}
                </div>
              </div>
            </q-td>
          </template>

          <!-- Status Column -->
          <template v-slot:body-cell-status="props">
            <q-td :props="props">
              <q-badge
                :color="props.row.status === 'aktif' ? 'green' : 'grey'"
                :label="props.row.status === 'aktif' ? 'Aktif' : 'Nonaktif'"
              />
            </q-td>
          </template>

          <!-- Actions Column -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <div class="row q-gutter-xs">
                <q-btn
                  icon="edit"
                  size="sm"
                  color="blue"
                  flat
                  dense
                  @click="editJadwal(props.row.id)"
                />
                <q-btn
                  :icon="props.row.status === 'aktif' ? 'pause' : 'play_arrow'"
                  :color="props.row.status === 'aktif' ? 'orange' : 'green'"
                  size="sm"
                  flat
                  dense
                  @click="toggleStatus(props.row)"
                />
                <q-btn
                  icon="delete"
                  size="sm"
                  color="red"
                  flat
                  dense
                  @click="deleteJadwal(props.row.id, props.row.wilayah)"
                />
              </div>
            </q-td>
          </template>

          <!-- Empty State -->
          <template v-slot:no-data>
            <div class="full-width row flex-center text-grey q-gutter-sm q-pa-xl">
              <q-icon name="calendar_today" size="3em" color="grey-4" />
              <div class="text-center">
                <div class="text-subtitle1 text-grey-7 q-mb-xs">Belum ada jadwal</div>
                <div class="text-caption text-grey-6">
                  {{
                    hasFilter
                      ? 'Tidak ada jadwal dengan filter yang dipilih'
                      : 'Mulai dengan membuat jadwal baru'
                  }}
                </div>
                <q-btn
                  v-if="!hasFilter"
                  label="Tambah Jadwal"
                  color="primary"
                  outline
                  class="q-mt-md"
                  :to="{ name: 'TambahJadwal' }"
                />
              </div>
            </div>
          </template>
        </q-table>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const $q = useQuasar()

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const loading = ref(true)
const jadwalList = ref([])

// Filter
const filter = ref({
  tanggal: '',
  status: '',
  search: '',
})

const statusOptions = [
  { label: 'Aktif', value: 'aktif' },
  { label: 'Nonaktif', value: 'nonaktif' },
]

// Columns
const columns = [
  {
    name: 'tanggal',
    label: 'Tanggal',
    field: 'tanggal',
    align: 'left',
    sortable: true,
    style: 'min-width: 150px;',
  },
  {
    name: 'jam',
    label: 'Jam',
    field: 'jam_mulai',
    align: 'left',
    sortable: true,
    style: 'min-width: 120px;',
  },
  {
    name: 'wilayah',
    label: 'Wilayah',
    field: 'wilayah',
    align: 'left',
    sortable: true,
    style: 'min-width: 300px;',
  },
  {
    name: 'status',
    label: 'Status',
    field: 'status',
    align: 'center',
    sortable: true,
    style: 'width: 100px;',
  },
  {
    name: 'actions',
    label: 'Aksi',
    align: 'center',
    style: 'width: 150px;',
  },
]

// Computed properties
const hasFilter = computed(() => {
  return filter.value.tanggal || filter.value.status || filter.value.search
})

// Tambahkan function ini di script setup
// Parse nama_petugas dari string yang dipisahkan koma
const getPetugasList = (namaPetugasString) => {
  if (!namaPetugasString || namaPetugasString.trim() === '') return []
  // Split by comma and trim each name
  return namaPetugasString
    .split(',')
    .map((p) => p.trim())
    .filter((p) => p !== '')
}

// Update filter search untuk include nama_petugas
const filteredJadwal = computed(() => {
  let filtered = jadwalList.value

  // Filter tanggal
  if (filter.value.tanggal) {
    filtered = filtered.filter((j) => {
      const jadwalDate = new Date(j.tanggal).toISOString().split('T')[0]
      return jadwalDate === filter.value.tanggal
    })
  }

  // Filter status
  if (filter.value.status) {
    filtered = filtered.filter((j) => j.status === filter.value.status)
  }

  // Filter search
  if (filter.value.search) {
    const search = filter.value.search.toLowerCase()
    filtered = filtered.filter(
      (j) =>
        (j.wilayah && j.wilayah.toLowerCase().includes(search)) ||
        (j.nama_petugas && j.nama_petugas.toLowerCase().includes(search)) || // Tambah pencarian petugas
        (j.keterangan && j.keterangan.toLowerCase().includes(search)),
    )
  }

  return filtered
})

const activeSchedules = computed(() => {
  return jadwalList.value.filter((j) => j.status === 'aktif').length
})

const todaySchedules = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return jadwalList.value.filter((j) => {
    const jadwalDate = new Date(j.tanggal).toISOString().split('T')[0]
    return jadwalDate === today
  }).length
})

const upcomingSchedules = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return jadwalList.value.filter((j) => {
    const jadwalDate = new Date(j.tanggal).toISOString().split('T')[0]
    return jadwalDate > today && j.status === 'aktif'
  }).length
})

// Helper functions
const formatDate = (dateString) => {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('id-ID', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    })
  } catch {
    return dateString
  }
}

const getDayName = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('id-ID', { weekday: 'long' })
  } catch {
    return ''
  }
}

const formatTime = (timeString) => {
  if (!timeString) return '-'
  // Jika waktu sudah dalam format 08:00:00, ambil hanya 08:00
  return timeString.slice(0, 5)
}

const calculateDuration = (start, end) => {
  if (!start || !end) return '-'

  try {
    const startTime = start.slice(0, 5)
    const endTime = end.slice(0, 5)

    const [startHour, startMinute] = startTime.split(':').map(Number)
    const [endHour, endMinute] = endTime.split(':').map(Number)

    let totalMinutes = endHour * 60 + endMinute - (startHour * 60 + startMinute)

    if (totalMinutes < 0) totalMinutes += 24 * 60

    const hours = Math.floor(totalMinutes / 60)
    const minutes = totalMinutes % 60

    if (hours === 0) return `${minutes} menit`
    if (minutes === 0) return `${hours} jam`
    return `${hours} jam ${minutes} menit`
  } catch {
    return '-'
  }
}

// Load data
// Load data
const loadJadwal = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')

    // PERUBAHAN DI SINI: gunakan endpoint /list bukan /
    const response = await axios.get(`${API_URL}/api/jadwal/list`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    console.log('Jadwal API Response:', response.data)

    if (response.data.success) {
      // Data dari endpoint /list sudah punya field nama_petugas (string gabungan)
      jadwalList.value = response.data.data.map((jadwal) => ({
        id: jadwal.id,
        tanggal: jadwal.tanggal,
        jam_mulai: jadwal.jam_mulai,
        jam_selesai: jadwal.jam_selesai,
        wilayah: jadwal.wilayah,
        keterangan: jadwal.keterangan,
        nama_petugas: jadwal.nama_petugas, // String gabungan "Nama1, Nama2, Nama3"
        status: jadwal.status || 'aktif',
      }))

      // Sort by tanggal descending (terbaru dulu)
      jadwalList.value.sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal))
    }
  } catch (error) {
    console.error('Error loading jadwal:', error)
    $q.notify({
      type: 'negative',
      message: error.response?.data?.message || 'Gagal memuat data jadwal',
      position: 'top',
    })
  } finally {
    loading.value = false
  }
}

// Actions
const editJadwal = (id) => {
  router.push(`/admin/jadwal/edit/${id}`)
}

const toggleStatus = async (jadwal) => {
  $q.dialog({
    title: 'Konfirmasi',
    message: `Apakah Anda yakin ingin ${jadwal.status === 'aktif' ? 'menonaktifkan' : 'mengaktifkan'} jadwal ini?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const token = localStorage.getItem('token')

      // PERUBAHAN: gunakan PATCH bukan PUT
      const response = await axios.patch(
        `${API_URL}/api/jadwal/${jadwal.id}/toggle-status`,
        {}, // Data kosong karena backend tidak butuh body
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )

      if (response.data.success) {
        $q.notify({
          type: 'positive',
          message:
            response.data.message ||
            `Jadwal berhasil ${jadwal.status === 'aktif' ? 'dinonaktifkan' : 'diaktifkan'}`,
          position: 'top',
        })
        await loadJadwal()
      }
    } catch (error) {
      console.error('Error toggling status:', error)
      $q.notify({
        type: 'negative',
        message: error.response?.data?.message || 'Gagal mengubah status jadwal',
        position: 'top',
      })
    }
  })
}

const deleteJadwal = async (id, wilayah) => {
  $q.dialog({
    title: 'Konfirmasi Hapus',
    message: `Yakin ingin menghapus jadwal untuk wilayah <strong>${wilayah || 'ini'}</strong>?`,
    html: true,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const token = localStorage.getItem('token')

      await axios.delete(`${API_URL}/api/jadwal/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      await loadJadwal()

      $q.notify({
        type: 'positive',
        message: 'Jadwal berhasil dihapus!',
        position: 'top',
      })
    } catch (error) {
      console.error(error)
      $q.notify({
        type: 'negative',
        message: error.response?.data?.message || 'Gagal menghapus jadwal',
        position: 'top',
      })
    }
  })
}

// Lifecycle
onMounted(() => {
  if (route.query.search) {
    filter.value.search = route.query.search
  }
  loadJadwal()
})
</script>

<style scoped>
.data-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.stat-card {
  border-radius: 12px;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}
</style>
