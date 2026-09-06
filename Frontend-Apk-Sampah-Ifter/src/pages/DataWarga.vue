<template>
  <q-page class="q-pa-md bg-green-1">
    <div class="row q-mb-md">
      <q-btn-toggle
        v-model="dataType"
        toggle-color="green"
        color="white"
        text-color="primary"
        :options="[
          { label: 'Data Petugas', value: 'petugas', to: { name: 'DataPetugas' } },
          { label: 'Data Warga', value: 'warga' },
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
        @click="goToAddWarga"
        class="q-px-md text-weight-bold rounded-btn"
      />
      <q-btn icon="refresh" color="grey" flat round @click="refreshData" />

      <q-input
        v-model="searchQuery"
        placeholder="Cari Warga..."
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
    <div class="row q-col-gutter-md q-mb-md" v-if="!loading && wargaList.length > 0">
      <div class="col-6 col-sm-3">
        <q-card class="stat-card text-center">
          <q-card-section>
            <div class="text-h6 text-primary">{{ wargaList.length }}</div>
            <div class="text-caption text-grey-7">Total Warga</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-6 col-sm-3">
        <q-card class="stat-card text-center">
          <q-card-section>
            <div class="text-h6 text-green">{{ rtCount }}</div>
            <div class="text-caption text-grey-7">RT Terdaftar</div>
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
    <q-card class="data-card" v-else>
      <q-card-section class="q-pb-none">
        <div class="text-weight-bold text-grey-8">Daftar Warga ({{ filteredWarga.length }})</div>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <div class="q-mt-sm">
          <div
            v-for="warga in filteredWarga"
            :key="warga.id"
            class="q-py-md data-item row items-center"
            style="border-bottom: 1px solid #eee"
          >
            <div class="col-auto q-pr-md">
              <q-avatar color="blue-1" text-color="blue-8" size="md">
                <q-icon name="person" />
              </q-avatar>
            </div>

            <div class="col">
              <div class="text-weight-bold text-dark">
                {{ warga.nama_warga }}
                <q-badge color="blue" outline class="q-ml-xs">
                  RT {{ warga.rt }}/RW {{ warga.rw }}
                </q-badge>
                <q-badge v-if="warga.saldo > 0" color="green" class="q-ml-xs">
                  Rp {{ formatCurrency(warga.saldo) }}
                </q-badge>
              </div>
              <div class="text-grey-7 text-caption q-mt-xs">
                <q-icon name="phone" size="12px" class="q-mr-xs" />
                {{ warga.no_telp || '-' }}
              </div>
              <div class="text-grey-7 text-caption">
                <q-icon name="email" size="12px" class="q-mr-xs" />
                {{ warga.email || '-' }}
              </div>
              <div class="text-grey-7 text-caption">
                <q-icon name="location_on" size="12px" class="q-mr-xs" />
                {{ warga.alamat || '-' }}
              </div>
            </div>

            <div class="col-auto">
              <div class="row q-gutter-xs">
                <q-btn
                  icon="location_on"
                  size="sm"
                  color="teal"
                  flat
                  dense
                  @click="showLocation(warga)"
                  title="Lihat Lokasi"
                />
                <q-btn
                  icon="account_balance_wallet"
                  size="sm"
                  color="green"
                  flat
                  dense
                  @click="topupSaldo(warga)"
                  title="Topup Saldo"
                />
                <q-btn icon="edit" size="sm" color="blue" flat dense @click="editItem(warga)" />
                <q-btn
                  icon="delete"
                  size="sm"
                  color="red"
                  flat
                  dense
                  @click="deleteItem(warga.id, warga.nama_warga)"
                />
              </div>
            </div>
          </div>

          <div v-if="filteredWarga.length === 0" class="text-center q-py-xl">
            <q-icon name="people" size="50px" color="grey-4" />
            <div class="text-h6 text-grey-5 q-mt-md">Tidak ada data warga</div>
            <div class="text-caption text-grey-6">
              {{
                searchQuery
                  ? `Tidak ditemukan warga dengan kata kunci "${searchQuery}"`
                  : 'Belum ada warga terdaftar'
              }}
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <!-- Modal untuk lihat lokasi -->
    <q-dialog v-model="showMapModal" persistent full-width>
      <q-card style="max-width: 800px">
        <q-card-section>
          <div class="text-h6">Lokasi {{ selectedWarga?.nama_warga }}</div>
          <div class="text-caption text-grey-7">
            RT {{ selectedWarga?.rt }}/RW {{ selectedWarga?.rw }} - {{ selectedWarga?.alamat }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="map-modal-container" ref="mapModalContainer"></div>

          <div class="row q-col-gutter-sm q-mt-sm">
            <div class="col-6">
              <q-input
                :model-value="selectedWarga?.latitude"
                label="Latitude"
                outlined
                dense
                readonly
                bg-color="grey-2"
              />
            </div>
            <div class="col-6">
              <q-input
                :model-value="selectedWarga?.longitude"
                label="Longitude"
                outlined
                dense
                readonly
                bg-color="grey-2"
              />
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Tutup" color="grey" v-close-popup />
          <q-btn label="Buka di Google Maps" color="primary" @click="openInGoogleMaps" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Map modal
const showMapModal = ref(false)
const selectedWarga = ref(null)
const mapModalContainer = ref(null)
let modalMap = null
let modalMarker = null

// Constants for default location
const DEFAULT_LAT = -7.09521
const DEFAULT_LNG = 107.484

const router = useRouter()
const $q = useQuasar()

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const dataType = ref('warga')
const searchQuery = ref('')
const wargaList = ref([])
const loading = ref(true)

// Fix untuk icon Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

// Format currency
const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID').format(value)
}

// Fetch data warga
const loadWarga = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')

    const res = await axios.get(`${API_URL}/api/warga/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (res.data.success) {
      wargaList.value = res.data.data.map((warga) => ({
        id: warga.id,
        nama_warga: warga.nama_lengkap,
        no_telp: warga.no_telp,
        alamat: warga.alamat_lengkap,
        rt: warga.rt || '-',
        rw: warga.rw || '-',
        kelurahan: warga.kelurahan,
        saldo: warga.saldo || 0,
        username: warga.username,
        email: warga.email,
        latitude: warga.latitude,
        longitude: warga.longitude,
      }))
    }
  } catch (err) {
    console.error('Gagal mengambil data warga:', err)
    console.error('DETAIL ERROR:', err.response?.data || err)

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
      message: err.response?.data?.message || 'Gagal mengambil data warga',
      position: 'top',
    })
  } finally {
    loading.value = false
  }
}

// Filter warga berdasarkan pencarian
const filteredWarga = computed(() => {
  if (!searchQuery.value.trim()) return wargaList.value

  const query = searchQuery.value.toLowerCase()
  return wargaList.value.filter((warga) => {
    return (
      warga.nama_warga?.toLowerCase().includes(query) ||
      warga.no_telp?.toLowerCase().includes(query) ||
      warga.email?.toLowerCase().includes(query) ||
      warga.rt?.includes(query) ||
      warga.rw?.includes(query)
    )
  })
})

// Computed properties untuk statistik
const rtCount = computed(() => {
  const rts = new Set(wargaList.value.map((w) => w.rt).filter((rt) => rt && rt !== '-'))
  return rts.size
})

// Hapus warga
const deleteItem = async (id, nama) => {
  $q.dialog({
    title: 'Konfirmasi Hapus',
    message: `Yakin ingin menghapus warga <strong>${nama}</strong>?`,
    html: true,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const token = localStorage.getItem('token')

      await axios.delete(`${API_URL}/api/warga/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      await loadWarga()

      $q.notify({
        type: 'positive',
        message: 'Warga berhasil dihapus!',
        position: 'top',
        timeout: 2000,
      })
    } catch (err) {
      console.error(err)

      let errorMessage = 'Gagal menghapus warga'
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

// Topup saldo
const topupSaldo = (warga) => {
  $q.dialog({
    title: 'Topup Saldo',
    message: `Topup saldo untuk <strong>${warga.nama_warga}</strong>`,
    html: true,
    prompt: {
      model: '',
      type: 'number',
      label: 'Jumlah (Rp)',
      hint: 'Masukkan jumlah topup',
      isValid: (val) => val > 0 || 'Harus lebih dari 0',
    },
    cancel: true,
    persistent: true,
  }).onOk(async (jumlah) => {
    try {
      const token = localStorage.getItem('token')

      const response = await axios.post(
        `${API_URL}/api/warga/${warga.id}/topup`,
        { jumlah: parseFloat(jumlah) },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )

      if (response.data.success) {
        $q.notify({
          type: 'positive',
          message: response.data.message,
          position: 'top',
        })
        await loadWarga()
      }
    } catch (error) {
      console.error('Topup error:', error)
      $q.notify({
        type: 'negative',
        message: error.response?.data?.message || 'Gagal topup saldo',
        position: 'top',
      })
    }
  })
}

// Navigasi
const goToAddWarga = () => {
  router.push({ name: 'TambahWarga' })
}

const editItem = (warga) => {
  router.push({
    name: 'EditWarga',
    params: { id: warga.id },
  })
}

const showLocation = (warga) => {
  selectedWarga.value = warga
  showMapModal.value = true

  // Initialize map in modal
  nextTick(() => {
    initModalMap()
  })
}

const initModalMap = () => {
  if (!mapModalContainer.value) return

  // Cleanup existing map
  if (modalMap) {
    modalMap.remove()
  }

  const lat = selectedWarga.value?.latitude || DEFAULT_LAT
  const lng = selectedWarga.value?.longitude || DEFAULT_LNG

  // Create map
  modalMap = L.map(mapModalContainer.value).setView([lat, lng], 16)

  // Add tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(modalMap)

  // Add marker
  modalMarker = L.marker([lat, lng]).addTo(modalMap)

  // Add popup
  modalMarker
    .bindPopup(
      `
    <b>${selectedWarga.value?.nama_warga}</b><br/>
    ${selectedWarga.value?.alamat || ''}<br/>
    RT ${selectedWarga.value?.rt}/RW ${selectedWarga.value?.rw}
  `,
    )
    .openPopup()

  // Fit map to container
  setTimeout(() => {
    modalMap.invalidateSize()
  }, 100)
}

const openInGoogleMaps = () => {
  if (!selectedWarga.value?.latitude || !selectedWarga.value?.longitude) return

  const url = `https://www.google.com/maps?q=${selectedWarga.value.latitude},${selectedWarga.value.longitude}`
  window.open(url, '_blank')
}

// Cleanup modal map
watch(showMapModal, (newVal) => {
  if (!newVal && modalMap) {
    setTimeout(() => {
      modalMap.remove()
      modalMap = null
    }, 500)
  }
})

const refreshData = () => {
  loadWarga()
}

// Lifecycle
onMounted(() => {
  loadWarga()
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

.map-modal-container {
  height: 400px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #e0e0e0;
}
</style>
