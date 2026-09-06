<template>
  <q-page class="q-pa-md bg-green-1">
    <div class="row q-mb-md">
      <!-- Di DataPetugas.vue, update q-btn-toggle -->
      <q-btn-toggle
        v-model="dataType"
        toggle-color="green"
        color="white"
        text-color="primary"
        :options="[
          { label: 'Data Petugas', value: 'petugas' },
          { label: 'Data Warga', value: 'warga', to: { name: 'DataWarga' } },
        ]"
        unelevated
        spread
        class="rounded-toggle"
      />
    </div>

    <div class="row items-center q-gutter-sm q-mb-md">
      <q-btn
        label="Tambah"
        color="yellow-8"
        text-color="black"
        unelevated
        @click="goToAddPetugas"
        class="q-px-md text-weight-bold rounded-btn"
      />
      <q-btn icon="refresh" color="grey" flat round @click="refreshData" />

      <q-input
        v-model="searchQuery"
        placeholder="Cari Petugas..."
        dense
        outlined
        clearable
        class="col search-input"
      >
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
    </div>

    <!-- Statistics Cards -->
    <div class="row q-col-gutter-md q-mb-md" v-if="!loading && petugasList.length > 0">
      <div class="col-6 col-sm-3">
        <q-card class="stat-card text-center">
          <q-card-section>
            <div class="text-h6 text-primary">{{ petugasList.length }}</div>
            <div class="text-caption text-grey-7">Total Petugas</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-6 col-sm-3">
        <q-card class="stat-card text-center">
          <q-card-section>
            <div class="text-h6 text-green">{{ activeCount }}</div>
            <div class="text-caption text-grey-7">Aktif</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-6 col-sm-3">
        <q-card class="stat-card text-center">
          <q-card-section>
            <div class="text-h6 text-red">{{ inactiveCount }}</div>
            <div class="text-caption text-grey-7">Tidak Aktif</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-6 col-sm-3">
        <q-card class="stat-card text-center">
          <q-card-section>
            <div class="text-h6 text-yellow-8">{{ totalKarung }}</div>
            <div class="text-caption text-grey-7">Total Karung</div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center q-py-lg">
      <q-spinner color="primary" size="2em" />
      <div class="text-grey-7 q-mt-sm">Memuat data...</div>
    </div>

    <!-- Data List -->
    <!-- Data List -->
    <q-card class="data-card" v-else>
      <q-card-section class="q-pb-none">
        <div class="text-weight-bold text-grey-8">
          Daftar Petugas ({{ filteredPetugas.length }})
        </div>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <!-- GANTI Q-LIST dengan DIV biasa -->
        <div class="q-mt-sm">
          <div
            v-for="petugas in filteredPetugas"
            :key="petugas.id"
            class="q-py-md data-item row items-center"
            style="border-bottom: 1px solid #eee"
          >
            <div class="col-auto q-pr-md">
              <q-avatar color="primary-1" text-color="primary-8" size="md">
                <q-icon name="support_agent" />
              </q-avatar>
            </div>

            <div class="col">
              <div class="text-weight-bold text-dark">
                {{ petugas.nama_petugas }}
                <q-badge
                  v-if="petugas.total_karung > 0"
                  color="yellow"
                  text-color="black"
                  class="q-ml-xs"
                >
                  {{ petugas.total_karung }} karung
                </q-badge>
              </div>
              <div class="text-grey-7 text-caption q-mt-xs">
                <q-icon name="phone" size="12px" class="q-mr-xs" />
                {{ petugas.no_telp || '-' }}
              </div>
              <div class="text-grey-7 text-caption">
                <q-icon name="email" size="12px" class="q-mr-xs" />
                {{ petugas.email || '-' }}
              </div>
              <div class="q-mt-xs">
                <q-badge
                  :color="getStatusColor(petugas.status)"
                  :label="petugas.status || 'Tidak Aktif'"
                  class="status-badge"
                />
              </div>
            </div>

            <div class="col-auto">
              <div class="row q-gutter-xs">
                <q-btn
                  label="Shift"
                  size="sm"
                  color="yellow-8"
                  text-color="black"
                  unelevated
                  dense
                  @click="assignShift(petugas)"
                />
                <q-btn icon="edit" size="sm" color="blue" flat dense @click="editItem(petugas)" />
                <q-btn
                  icon="delete"
                  size="sm"
                  color="red"
                  flat
                  dense
                  @click="deleteItem(petugas.id, petugas.nama_petugas)"
                />
              </div>
            </div>
          </div>

          <div v-if="filteredPetugas.length === 0" class="text-center q-py-xl">
            <q-icon name="people" size="50px" color="grey-4" />
            <div class="text-h6 text-grey-5 q-mt-md">Tidak ada data petugas</div>
            <div class="text-caption text-grey-6">
              {{
                searchQuery
                  ? `Tidak ditemukan petugas dengan kata kunci "${searchQuery}"`
                  : 'Belum ada petugas terdaftar'
              }}
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'

const router = useRouter()
const $q = useQuasar()

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const dataType = ref('petugas')
const searchQuery = ref('')
const petugasList = ref([])
const loading = ref(true)

// Helper function untuk warna status
const getStatusColor = (status) => {
  switch (status?.toLowerCase()) {
    case 'aktif':
      return 'green'
    case 'cuti':
      return 'orange'
    case 'resign':
      return 'red'
    default:
      return 'grey'
  }
}

// Fetch data petugas
const loadPetugas = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')

    const res = await axios.get(`${API_URL}/api/petugas/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (res.data.success) {
      petugasList.value = res.data.data.map((petugas) => ({
        id: petugas.id,
        nama_petugas: petugas.nama_petugas || petugas.nama_lengkap,
        no_telp: petugas.no_telp || petugas.no_telepon,
        alamat: petugas.alamat,
        status: petugas.status || 'Tidak Aktif',
        gaji_per_karung: petugas.gaji_per_karung,
        username: petugas.username,
        email: petugas.email,
        total_karung: petugas.total_karung || 0,
      }))
    }
  } catch (err) {
    console.error('Gagal mengambil data petugas:', err)

    if (err.response?.status === 401) {
      $q.notify({
        type: 'negative',
        message: 'Sesi telah berakhir, silakan login kembali',
        position: 'top',
      })
      router.push('/login')
      return
    }

    $q.notify({
      type: 'negative',
      message: err.response?.data?.message || 'Gagal mengambil data petugas',
      position: 'top',
    })
  } finally {
    loading.value = false
  }
}

// Filter petugas berdasarkan pencarian
const filteredPetugas = computed(() => {
  if (!searchQuery.value.trim()) return petugasList.value

  const query = searchQuery.value.toLowerCase()
  return petugasList.value.filter((petugas) => {
    return (
      petugas.nama_petugas?.toLowerCase().includes(query) ||
      petugas.no_telp?.toLowerCase().includes(query) ||
      petugas.status?.toLowerCase().includes(query) ||
      petugas.email?.toLowerCase().includes(query)
    )
  })
})

// Computed properties untuk statistik
const activeCount = computed(() => {
  return petugasList.value.filter((p) => p.status?.toLowerCase() === 'aktif').length
})

const inactiveCount = computed(() => {
  return petugasList.value.filter((p) => p.status?.toLowerCase() !== 'aktif').length
})

const totalKarung = computed(() => {
  return petugasList.value.reduce((sum, p) => sum + (p.total_karung || 0), 0)
})

// Hapus petugas
const deleteItem = async (id, nama) => {
  $q.dialog({
    title: 'Konfirmasi Hapus',
    message: `Yakin ingin menghapus petugas <strong>${nama}</strong>?`,
    html: true,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const token = localStorage.getItem('token')

      await axios.delete(`${API_URL}/api/petugas/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      await loadPetugas()

      $q.notify({
        type: 'positive',
        message: 'Petugas berhasil dihapus!',
        position: 'top',
        timeout: 2000,
      })
    } catch (err) {
      console.error(err)

      let errorMessage = 'Gagal menghapus petugas'
      if (err.response?.data?.message) {
        errorMessage = err.response.data.message
      }

      $q.notify({
        type: 'negative',
        message: errorMessage,
        position: 'top',
      })
    }
  })
}

// Navigasi
const goToAddPetugas = () => {
  router.push({ name: 'TambahPetugas' })
}

const editItem = (petugas) => {
  router.push({
    name: 'EditPetugas',
    params: { id: petugas.id },
  })
}

const assignShift = (petugas) => {
  router.push({
    name: 'JadwalPetugas',
    params: { id: petugas.id },
    query: { nama: petugas.nama_petugas },
  })
}

const refreshData = () => {
  loadPetugas()
}

// Lifecycle
onMounted(() => {
  loadPetugas()
})
</script>

<style scoped>
.q-page {
  background-color: #f8faf9 !important;
}

.rounded-toggle {
  border-radius: 12px;
  border: 1px solid #006837;
}

.rounded-btn {
  border-radius: 12px;
}

.rounded-btn-sm {
  border-radius: 8px;
}

.search-input :deep(.q-field__control) {
  border-radius: 12px;
  background: white;
}

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

.data-item {
  border-radius: 8px;
  margin-bottom: 4px;
  transition: all 0.2s ease;
}

.data-item:hover {
  background-color: #f5f9f7;
}

.status-badge {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 10px;
  font-weight: 500;
}

.text-primary {
  color: #006837 !important;
}

/* FIX: Pastikan button bisa diklik */
:deep(.q-item__section--side) {
  pointer-events: auto !important;
}

.action-btn {
  cursor: pointer !important;
}
</style>
