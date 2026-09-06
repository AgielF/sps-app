<template>
  <q-page class="q-pa-md bg-green-1">
    <div class="row items-center q-mb-md">
      <q-btn flat round icon="arrow_back" @click="goBack" />
      <div class="text-h6 q-ml-md text-weight-bold text-dark">
        {{ isEdit ? 'Edit Jadwal' : 'Tambah Jadwal Pengambilan' }}
      </div>
    </div>

    <q-form @submit="onSubmit" class="q-gutter-y-md">
      <q-card class="form-card">
        <q-card-section>
          <div class="text-subtitle1 text-weight-bold q-mb-sm">Informasi Jadwal</div>

          <!-- Tanggal -->
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.tanggal"
                label="Tanggal"
                outlined
                dense
                type="date"
                :rules="[(val) => !!val || 'Tanggal wajib diisi']"
                :min="minDate"
              >
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                      <q-date v-model="form.tanggal" mask="YYYY-MM-DD" />
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-6">
              <q-select
                v-model="form.status"
                label="Status"
                outlined
                dense
                :options="statusOptions"
                :rules="[(val) => !!val || 'Status wajib dipilih']"
              />
            </div>
          </div>

          <!-- Jam -->
          <div class="row q-col-gutter-md q-mt-sm">
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.jam_mulai"
                label="Jam Mulai"
                outlined
                dense
                type="time"
                :rules="[(val) => !!val || 'Jam mulai wajib diisi']"
              />
            </div>
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.jam_selesai"
                label="Jam Selesai"
                outlined
                dense
                type="time"
                :rules="[(val) => !!val || 'Jam selesai wajib diisi']"
              />
            </div>
          </div>

          <!-- Petugas Bertugas (Multiple Selection) -->
          <div class="q-mt-sm">
            <q-select
              v-model="form.petugas_ids"
              label="Petugas Bertugas"
              multiple
              outlined
              dense
              :options="petugasOptions"
              option-label="nama"
              option-value="id"
              emit-value
              map-options
              :rules="[(val) => (val && val.length > 0) || 'Minimal pilih 1 petugas']"
              use-chips
            >
              <template v-slot:selected-item="scope">
                <q-chip
                  dense
                  removable
                  @remove="removePetugas(scope.opt.id)"
                  color="primary"
                  text-color="white"
                  class="q-ma-xs"
                >
                  {{ scope.opt.nama }}
                </q-chip>
              </template>

              <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                  <q-item-section avatar>
                    <q-avatar color="primary" text-color="white">
                      {{ scope.opt.nama.charAt(0) }}
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ scope.opt.nama }}</q-item-label>
                    <q-item-label caption>{{ scope.opt.no_telepon }}</q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>

          <!-- Wilayah -->
          <div class="q-mt-sm">
            <q-input
              v-model="form.wilayah"
              label="Wilayah/Lokasi"
              outlined
              dense
              type="textarea"
              rows="2"
              placeholder="Contoh: Perumahan Griya Asri, RT 01-05, Kelurahan Suraja"
              :rules="[(val) => !!val || 'Wilayah wajib diisi']"
            />
          </div>

          <!-- Keterangan -->
          <div class="q-mt-sm">
            <q-input
              v-model="form.keterangan"
              label="Keterangan"
              outlined
              dense
              type="textarea"
              rows="2"
              placeholder="Catatan tambahan tentang jadwal (opsional)"
            />
          </div>
        </q-card-section>

        <q-card-actions class="q-pa-md">
          <q-btn label="Batal" color="grey" flat @click="goBack" class="q-mr-sm" />
          <q-space />
          <q-btn
            :label="isEdit ? 'Update' : 'Simpan'"
            color="primary"
            type="submit"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-form>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const $q = useQuasar()

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const isEdit = ref(false)
const loading = ref(false)
const petugasList = ref([])

// Options
const statusOptions = [
  { label: 'Aktif', value: 'aktif' },
  { label: 'Nonaktif', value: 'nonaktif' },
]

// Form data
const form = ref({
  tanggal: '',
  jam_mulai: '08:00',
  jam_selesai: '12:00',
  wilayah: '',
  keterangan: '',
  status: 'aktif',
  petugas_ids: [], // Array of petugas IDs
})

// Petugas options from database
const petugasOptions = computed(() => {
  return petugasList.value.map((petugas) => ({
    id: petugas.id,
    nama:
      petugas.nama_lengkap || petugas.nama_petugas || petugas.username || `Petugas ${petugas.id}`,
    no_telepon: petugas.no_telepon || petugas.no_telp || '-',
  }))
})

// Minimum date for date picker (today)
const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// Load petugas data
// Di loadPetugas, tambahkan debugging:
const loadPetugas = async () => {
  try {
    const token = localStorage.getItem('token')
    console.log('Loading petugas...')

    const response = await axios.get(`${API_URL}/api/petugas/`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    console.log('Petugas API Response:', response.data)

    if (response.data.success) {
      petugasList.value = response.data.data
      console.log('Petugas loaded:', petugasList.value)
      console.log('Total petugas:', petugasList.value.length)
    } else {
      console.error('Petugas API not successful:', response.data)
    }
  } catch (error) {
    console.error('Error loading petugas:', error)
    console.error('Error details:', error.response?.data || error.message)

    $q.notify({
      type: 'negative',
      message: 'Gagal memuat data petugas',
      position: 'top',
    })
  }
}

// Load jadwal data for edit
// Load jadwal data for edit
const loadJadwalData = async (id) => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    console.log(`Loading jadwal data for ID: ${id}`)

    const response = await axios.get(`${API_URL}/api/jadwal/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    console.log('API Response for jadwal detail:', response.data)

    if (response.data.success) {
      const data = response.data.data

      // Debug log untuk melihat struktur data
      console.log('Raw data from API:', data)
      console.log('Petugas IDs from API:', data.petugas_ids)

      // Format tanggal untuk input date
      const tanggal = data.tanggal ? data.tanggal.split('T')[0] : ''

      form.value = {
        tanggal: tanggal,
        jam_mulai: data.jam_mulai?.slice(0, 5) || '08:00',
        jam_selesai: data.jam_selesai?.slice(0, 5) || '12:00',
        wilayah: data.wilayah || '',
        keterangan: data.keterangan || '',
        status: data.status || 'aktif',
        petugas_ids: data.petugas_ids || [], // <-- PERUBAHAN DI SINI
      }

      console.log('Form setelah diisi:', form.value)
    } else {
      console.error('API tidak success:', response.data)
      $q.notify({
        type: 'negative',
        message: response.data.message || 'Gagal memuat data jadwal',
        position: 'top',
      })
    }
  } catch (error) {
    console.error('Error loading jadwal:', error)
    console.error('Error details:', {
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url,
    })

    $q.notify({
      type: 'negative',
      message: error.response?.data?.message || 'Gagal memuat data jadwal',
      position: 'top',
    })
  } finally {
    loading.value = false
  }
}

// Remove petugas from selection
const removePetugas = (petugasId) => {
  form.value.petugas_ids = form.value.petugas_ids.filter((id) => id !== petugasId)
}

// On mount
// Di onMounted, tambahkan:
onMounted(async () => {
  console.log('=== DEBUG MODE ===')
  console.log('Route name:', route.name)
  console.log('Route params:', route.params)
  console.log('Route path:', route.path)
  console.log('Is edit mode?', route.name === 'EditJadwal' && route.params.id)

  await loadPetugas()

  if (route.name === 'EditJadwal' && route.params.id) {
    isEdit.value = true
    console.log('Loading edit mode for jadwal ID:', route.params.id)

    // Coba langsung hit API untuk debug
    try {
      const token = localStorage.getItem('token')
      const testResponse = await axios.get(`${API_URL}/api/jadwal/${route.params.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      console.log('TEST API Response:', testResponse.data)
    } catch (testError) {
      console.error('TEST API Error:', testError.response?.data || testError.message)
    }

    await loadJadwalData(route.params.id)
  } else {
    console.log('Add mode - no ID found')
  }
})
// Submit form
async function onSubmit() {
  console.log('Submitting form...', form.value)

  // Validasi
  if (
    !form.value.tanggal ||
    !form.value.jam_mulai ||
    !form.value.jam_selesai ||
    !form.value.wilayah
  ) {
    $q.notify({
      type: 'warning',
      message: 'Tanggal, jam, dan wilayah wajib diisi',
      position: 'top',
    })
    return
  }

  // Validasi petugas
  if (form.value.petugas_ids.length === 0) {
    $q.notify({
      type: 'warning',
      message: 'Minimal pilih 1 petugas',
      position: 'top',
    })
    return
  }

  // Validasi jam
  if (form.value.jam_mulai >= form.value.jam_selesai) {
    $q.notify({
      type: 'warning',
      message: 'Jam mulai harus lebih awal dari jam selesai',
      position: 'top',
    })
    return
  }

  loading.value = true

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      $q.notify({
        type: 'negative',
        message: 'Token tidak ditemukan. Silakan login kembali.',
        position: 'top',
      })
      router.push('/login')
      return
    }

    // Format data untuk dikirim
    const dataToSend = {
      tanggal: form.value.tanggal,
      jam_mulai: form.value.jam_mulai,
      jam_selesai: form.value.jam_selesai,
      wilayah: form.value.wilayah,
      keterangan: form.value.keterangan || '',
      status: form.value.status,
      petugas_ids: form.value.petugas_ids, // Array petugas IDs
    }

    console.log('Data to send to API:', dataToSend)

    let response
    let url

    if (isEdit.value) {
      // PATCH untuk update - ke endpoint /api/jadwal/<id>
      url = `${API_URL}/api/jadwal/${route.params.id}`
      console.log('UPDATE URL:', url)

      response = await axios.patch(url, dataToSend, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
    } else {
      // POST untuk create - ke endpoint /api/jadwal/multi
      url = `${API_URL}/api/jadwal/multi`
      console.log('CREATE URL:', url)

      response = await axios.post(url, dataToSend, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
    }

    console.log('API Response:', response.data)

    if (response.data.success) {
      $q.notify({
        type: 'positive',
        message:
          response.data.message ||
          (isEdit.value ? 'Jadwal berhasil diupdate!' : 'Jadwal baru berhasil ditambahkan!'),
        position: 'top',
        timeout: 3000,
      })

      setTimeout(() => {
        router.push('/admin/jadwal')
      }, 1000)
    } else {
      $q.notify({
        type: 'warning',
        message: response.data.message || 'Gagal menyimpan jadwal',
        position: 'top',
      })
    }
  } catch (error) {
    console.error('Error saving jadwal:', error)
    console.error('Error response:', error.response?.data)
    console.error('Error status:', error.response?.status)
    console.error('Error URL:', error.config?.url)
    console.error('Error method:', error.config?.method)

    let errorMessage = 'Terjadi kesalahan saat menyimpan jadwal'

    // Jika error 405, beri pesan spesifik
    if (error.response?.status === 405) {
      errorMessage = 'Method HTTP tidak diizinkan. Silakan periksa endpoint API.'
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.response?.data?.errors) {
      errorMessage = Array.isArray(error.response.data.errors)
        ? error.response.data.errors.join(', ')
        : error.response.data.errors
    } else if (error.message) {
      errorMessage = error.message
    }

    $q.notify({
      type: 'negative',
      message: errorMessage,
      position: 'top',
      timeout: 5000,
    })
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.form-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}
</style>
