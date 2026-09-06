<template>
  <q-page class="q-pa-md bg-green-1">
    <!-- Header -->
    <div class="row items-center q-mb-lg">
      <div class="col">
        <div class="text-h6 text-weight-bold text-dark-green">
          Form Pengajuan Pengambilan Sampah
        </div>
        <div class="text-caption text-grey-7">
          Isi formulir berikut untuk mengajukan pengambilan sampah
        </div>
      </div>
      <div class="col-auto">
        <q-btn icon="arrow_back" color="grey" flat round @click="$router.go(-1)" />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center q-py-xl">
      <q-spinner color="primary" size="2em" />
      <div class="text-grey-7 q-mt-sm">Memuat data...</div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="q-pa-md bg-red-1 rounded-borders q-mb-md">
      <div class="text-red text-weight-medium">
        <q-icon name="error" class="q-mr-xs" />
        {{ error }}
      </div>
      <div class="text-caption text-red-7 q-mt-xs">{{ errorDetail }}</div>
      <q-btn
        label="Kembali ke Dashboard"
        color="red"
        flat
        dense
        to="/user/dashboard"
        class="q-mt-sm"
      />
    </div>

    <!-- Main Form -->
    <div v-else class="row justify-center">
      <div class="col-12 col-md-8 col-lg-6">
        <q-card class="form-card q-mb-lg">
          <q-card-section>
            <!-- Jadwal Info -->
            <div class="jadwal-info q-mb-lg">
              <div class="text-subtitle1 text-weight-bold text-dark-green q-mb-sm">
                Informasi Jadwal
              </div>
              <div class="row q-col-gutter-md">
                <div class="col-6">
                  <div class="info-item">
                    <div class="text-caption text-grey-7">Tanggal</div>
                    <div class="text-body1 text-weight-medium">
                      {{ formatDate(jadwalData.tanggal) }}
                    </div>
                  </div>
                </div>
                <div class="col-6">
                  <div class="info-item">
                    <div class="text-caption text-grey-7">Wilayah</div>
                    <div class="text-body1 text-weight-medium">
                      {{ jadwalData.wilayah }}
                    </div>
                  </div>
                </div>
                <div class="col-6">
                  <div class="info-item">
                    <div class="text-caption text-grey-7">Waktu</div>
                    <div class="text-body1 text-weight-medium">
                      {{ jadwalData.jam_mulai }} - {{ jadwalData.jam_selesai }}
                    </div>
                  </div>
                </div>
                <div class="col-6">
                  <div class="info-item">
                    <div class="text-caption text-grey-7">Petugas</div>
                    <div class="text-body1 text-weight-medium">
                      {{ jadwalData.nama_petugas || 'Akan ditugaskan' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Info Warga -->
            <div class="warga-info q-mb-lg bg-blue-1 q-pa-md rounded-borders">
              <div class="text-subtitle1 text-weight-bold text-dark-green q-mb-sm">Data Warga</div>
              <div class="row q-col-gutter-md">
                <div class="col-6">
                  <div class="info-item">
                    <div class="text-caption text-grey-7">Nama</div>
                    <div class="text-body1 text-weight-medium">
                      {{ wargaData.nama_warga }}
                    </div>
                  </div>
                </div>
                <div class="col-6">
                  <div class="info-item">
                    <div class="text-caption text-grey-7">No. Telepon</div>
                    <div class="text-body1 text-weight-medium">
                      {{ wargaData.no_telepon }}
                    </div>
                  </div>
                </div>
                <div class="col-12">
                  <div class="info-item">
                    <div class="text-caption text-grey-7">Alamat</div>
                    <div class="text-body1 text-weight-medium">
                      {{ wargaData.alamat_lengkap }} RT {{ wargaData.rt }}/RW {{ wargaData.rw }},
                      {{ wargaData.wilayah }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Form Pengajuan -->
            <q-form @submit="submitPengajuan" class="q-gutter-md">
              <!-- Jenis Sampah (tetap sama) -->
              <div class="q-mb-md">
                <div class="text-subtitle2 text-weight-bold q-mb-sm">Jenis Sampah</div>
                <div class="text-caption text-grey-7 q-mb-md">
                  Pilih jenis sampah yang akan diambil (bisa lebih dari satu)
                </div>

                <div class="row q-col-gutter-sm">
                  <div
                    v-for="jenis in jenisSampahOptions"
                    :key="jenis.value"
                    class="col-6 col-sm-4"
                  >
                    <q-card
                      class="jenis-card cursor-pointer"
                      :class="{ selected: form.jenis_sampah.includes(jenis.value) }"
                      @click="toggleJenisSampah(jenis.value)"
                    >
                      <q-card-section class="text-center q-pa-sm">
                        <q-icon :name="jenis.icon" size="md" :color="jenis.color" class="q-mb-xs" />
                        <div class="text-caption text-weight-medium">{{ jenis.label }}</div>
                        <div class="text-caption text-grey-7">{{ jenis.desc }}</div>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>

                <!-- Custom Input -->
                <div class="q-mt-md">
                  <q-input
                    v-model="form.jenis_lainnya"
                    label="Jenis Sampah Lainnya"
                    outlined
                    dense
                    placeholder="Masukkan jenis sampah lainnya..."
                    :disable="form.jenis_sampah.length === 0"
                  />
                </div>
              </div>

              <!-- Estimasi Volume (tetap sama) -->
              <div class="q-mb-md">
                <div class="text-subtitle2 text-weight-bold q-mb-sm">Estimasi Volume Sampah</div>

                <q-radio
                  v-model="form.estimasi_volume"
                  val="sedikit"
                  label="Sedikit (1-2 kantong)"
                  class="q-mb-xs"
                />
                <q-radio
                  v-model="form.estimasi_volume"
                  val="sedang"
                  label="Sedang (3-5 kantong)"
                  class="q-mb-xs"
                />
                <q-radio v-model="form.estimasi_volume" val="banyak" label="Banyak (6+ kantong)" />
              </div>

              <!-- Keterangan Tambahan -->
              <div class="q-mb-md">
                <q-input
                  v-model="form.keterangan"
                  label="Keterangan Tambahan"
                  outlined
                  type="textarea"
                  rows="2"
                  placeholder="Contoh: Sampah sudah dipilah, ada sampah besar, lokasi khusus, dll..."
                />
              </div>

              <!-- Upload Foto (tetap sama) -->
              <div class="q-mb-lg">
                <div class="text-subtitle2 text-weight-bold q-mb-sm">Foto Sampah (Opsional)</div>
                <div class="text-caption text-grey-7 q-mb-sm">
                  Upload foto sampah untuk membantu petugas
                </div>

                <div
                  class="upload-area q-pa-lg text-center cursor-pointer rounded-borders bg-grey-2"
                  @click="triggerFileUpload"
                >
                  <input
                    ref="fileInput"
                    type="file"
                    accept="image/*"
                    style="display: none"
                    @change="handleFileUpload"
                  />

                  <q-icon name="cloud_upload" size="48px" color="grey-5" class="q-mb-sm" />
                  <div class="text-subtitle2 text-grey-7">Klik untuk upload foto</div>
                  <div class="text-caption text-grey-6">Maksimal 2MB, format JPG/PNG</div>
                </div>

                <!-- Preview Foto -->
                <div v-if="form.foto_sampah" class="q-mt-sm">
                  <div class="text-caption text-grey-7 q-mb-xs">Preview:</div>
                  <div class="photo-preview">
                    <q-img
                      :src="form.foto_sampah"
                      style="height: 100px; width: 100px"
                      class="rounded-borders"
                    />
                    <q-btn
                      icon="close"
                      size="sm"
                      flat
                      round
                      color="red"
                      class="remove-photo"
                      @click="removePhoto"
                    />
                  </div>
                </div>
              </div>

              <!-- Form Actions -->
              <div class="row q-col-gutter-sm">
                <div class="col-6">
                  <q-btn
                    label="Batal"
                    color="grey"
                    class="full-width"
                    :to="{ name: 'UserDashboard' }"
                  />
                </div>
                <div class="col-6">
                  <q-btn
                    label="Ajukan"
                    color="primary"
                    class="full-width"
                    type="submit"
                    :loading="submitting"
                    :disable="!isFormValid"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>

        <!-- Info Penting -->
        <q-card class="info-card">
          <q-card-section>
            <div class="text-subtitle2 text-weight-bold text-dark-green q-mb-sm">
              📌 Informasi Penting
            </div>
            <ul class="info-list">
              <li>Data alamat, RT/RW, dan kontak diambil dari profil warga</li>
              <li>Waktu pengambilan mengikuti jadwal yang dipilih</li>
              <li>Sampah harus sudah dipilah sesuai jenisnya sebelum pengambilan</li>
              <li>Pastikan sampah dalam kantong yang tertutup rapat</li>
              <li>Petugas akan menghubungi 1-2 jam sebelum pengambilan</li>
              <li>Pengajuan akan diverifikasi oleh petugas terlebih dahulu</li>
            </ul>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Success Dialog -->
    <q-dialog v-model="showSuccessDialog" persistent>
      <q-card class="success-dialog">
        <q-card-section class="text-center">
          <q-avatar color="green" text-color="white" size="lg" class="q-mb-sm">
            <q-icon name="check" />
          </q-avatar>
          <div class="text-h6 text-weight-bold text-green q-mb-sm">Pengajuan Berhasil!</div>
          <div class="text-body2 text-grey-7 q-mb-md">
            Pengajuan pengambilan sampah Anda telah dikirim. Petugas akan menghubungi atau ke rumah.
          </div>
          <div class="text-caption text-grey-6">
            Kode Pengajuan: <strong>{{ kodePengajuan }}</strong>
          </div>
        </q-card-section>

        <q-card-actions align="center" class="q-pb-md">
          <q-btn
            label="Kembali ke Dashboard"
            color="primary"
            unelevated
            :to="{ name: 'UserDashboard' }"
            class="q-px-lg"
          />
          <q-btn
            label="Lihat Status"
            color="green"
            flat
            :to="{ name: 'UserDashboard' }"
            class="q-px-lg"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router' // Tambah useRouter
import { date } from 'quasar'
import axios from 'axios'

const route = useRoute()
//const router = useRouter() // Inisialisasi router
const API_URL = 'http://127.0.0.1:5000'

// Refs
const loading = ref(true)
const error = ref('')
const errorDetail = ref('')
const submitting = ref(false)
const showSuccessDialog = ref(false)
const kodePengajuan = ref('')
const fileInput = ref(null)

// Data
const jadwalData = ref({
  id: null,
  tanggal: '',
  wilayah: '',
  jam_mulai: '',
  jam_selesai: '',
  nama_petugas: '',
})

const wargaData = ref({
  id: null,
  nama_warga: '',
  alamat: '',
  no_telepon: '',
  rt: '',
  rw: '',
  wilayah: '',
})

// Form Data - HAPUS field yang sudah ada di warga
const form = ref({
  id_jadwal: '',
  id_warga: '',
  jenis_sampah: [],
  jenis_lainnya: '',
  estimasi_volume: 'sedang',
  keterangan: '',
  foto_sampah: null,
  // HAPUS: alamat_detail, rt, rw, nomor_hp, nama_pemohon, waktu_pengambilan
})

// Options
const jenisSampahOptions = ref([
  {
    value: 'organik',
    label: 'Organik',
    desc: 'Sisa makanan, daun, dll',
    icon: 'grass',
    color: 'green',
  },
  {
    value: 'anorganik',
    label: 'Anorganik',
    desc: 'Plastik, kertas, logam',
    icon: 'recycling',
    color: 'blue',
  },
  {
    value: 'b3',
    label: 'B3',
    desc: 'Baterai, elektronik',
    icon: 'warning',
    color: 'red',
  },
  {
    value: 'kertas',
    label: 'Kertas',
    desc: 'Koran, kardus, buku',
    icon: 'description',
    color: 'brown',
  },
  {
    value: 'plastik',
    label: 'Plastik',
    desc: 'Botol, kemasan',
    icon: 'water_bottle',
    color: 'teal',
  },
  {
    value: 'logam',
    label: 'Logam',
    desc: 'Kaleng, besi',
    icon: 'handyman',
    color: 'orange',
  },
])

// HAPUS waktuOptions karena sudah diambil dari jadwal

// Computed - HAPUS validasi untuk field yang dihapus
const isFormValid = computed(() => {
  return (
    form.value.jenis_sampah.length > 0 && form.value.estimasi_volume
    // HAPUS validasi untuk: alamat_detail, rt, rw, nomor_hp, nama_pemohon, waktu_pengambilan
  )
})

// Methods
const formatDate = (dateString) => {
  if (!dateString) return '-'
  try {
    return date.formatDate(dateString, 'dddd, D MMMM YYYY')
  } catch {
    return dateString
  }
}

const toggleJenisSampah = (jenis) => {
  const index = form.value.jenis_sampah.indexOf(jenis)
  if (index === -1) {
    form.value.jenis_sampah.push(jenis)
  } else {
    form.value.jenis_sampah.splice(index, 1)
  }
}

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validasi file
  if (file.size > 2 * 1024 * 1024) {
    // 2MB
    alert('Ukuran file maksimal 2MB')
    return
  }

  if (!file.type.startsWith('image/')) {
    alert('Hanya file gambar yang diperbolehkan')
    return
  }

  // Convert to base64
  const reader = new FileReader()
  reader.onload = (e) => {
    form.value.foto_sampah = e.target.result
  }
  reader.readAsDataURL(file)
}

const removePhoto = () => {
  form.value.foto_sampah = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// Fetch Data
const fetchJadwalData = async () => {
  const id_jadwal = route.query.id_jadwal
  if (!id_jadwal) {
    throw new Error('ID jadwal tidak ditemukan')
  }

  const token = localStorage.getItem('token')
  const response = await axios.get(`${API_URL}/api/jadwal/${id_jadwal}`, {
    headers: { Authorization: `Bearer ${token}` },
  })

  if (response.data.success) {
    jadwalData.value = {
      id: id_jadwal,
      tanggal: response.data.data.tanggal,
      wilayah: response.data.data.wilayah,
      jam_mulai: response.data.data.jam_mulai?.substring(0, 5) || '08:00',
      jam_selesai: response.data.data.jam_selesai?.substring(0, 5) || '13:00',
      nama_petugas: response.data.data.nama_lengkap,
    }
    form.value.id_jadwal = id_jadwal
  } else {
    throw new Error(response.data.message || 'Gagal mengambil data jadwal')
  }
}

// Fetch data warga dengan token
const fetchWargaData = async () => {
  // AMBIL DARI LOCALSTORAGE SAJA - PASTI ADA KARENA BACKEND KIRIM LENGKAP
  const userData = JSON.parse(localStorage.getItem('userData'))

  console.log('Data warga dari localStorage:', userData)

  // Data HARUS LENGKAP dari backend
  wargaData.value = {
    id: userData.warga_id || userData.id, // warga_id dari backend
    nama_warga: userData.nama,
    alamat: userData.alamat, // dari backend
    no_telepon: userData.no_telepon,
    rt: userData.rt, // dari backend
    rw: userData.rw, // dari backend
    wilayah: userData.wilayah, // dari backend
  }

  form.value.id_warga = wargaData.value.id

  console.log('Data warga untuk form:', wargaData.value)
}

const submitPengajuan = async () => {
  submitting.value = true
  error.value = ''
  errorDetail.value = ''

  try {
    const token = localStorage.getItem('token')

    if (!token) {
      throw new Error('Token tidak ditemukan. Silakan login kembali')
    }

    console.log('=== SUBMIT DEBUG ===')
    console.log('Token:', token.substring(0, 20) + '...')

    // Pastikan data valid
    if (!wargaData.value.id) {
      throw new Error('Data warga tidak valid')
    }

    if (!form.value.id_jadwal) {
      throw new Error('Jadwal tidak valid')
    }

    // Siapkan data
    const submissionData = {
      id_jadwal: form.value.id_jadwal || 1,
      id_warga: wargaData.value.id || 1,
      jenis_sampah: form.value.jenis_sampah.join(', ') || 'organik',
      jenis_lainnya: form.value.jenis_lainnya || '',
      estimasi_volume: form.value.estimasi_volume || 'sedang',
      alamat_detail: `${wargaData.value.alamat} RT ${wargaData.value.rt}/RW ${wargaData.value.rw}, ${wargaData.value.wilayah}`,

      rt: wargaData.value.rt || '01',
      rw: wargaData.value.rw || '01',
      nomor_hp: wargaData.value.no_telepon || '081234567890',
      nama_pemohon: wargaData.value.nama_warga || 'Warga',
      keterangan: form.value.keterangan || '',
      waktu_pengambilan: 'pagi',
      foto_sampah: form.value.foto_sampah || null,
      status: 'menunggu',
    }

    console.log('Data to send:', submissionData)

    // Coba dengan fetch terlebih dahulu
    const response = await fetch(`${API_URL}/api/laporan`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(submissionData),
    })

    console.log('Response status:', response.status)

    const data = await response.json()
    console.log('Response data:', data)

    if (response.ok && data.success) {
      kodePengajuan.value = data.data?.kode_laporan || 'LAP-' + Date.now()
      showSuccessDialog.value = true

      // Clear form
      form.value.jenis_sampah = []
      form.value.jenis_lainnya = ''
      form.value.estimasi_volume = 'sedang'
      form.value.keterangan = ''
      form.value.foto_sampah = null
    } else {
      if (data.errors && data.errors.length > 0) {
        throw new Error(data.errors.join(', '))
      } else {
        throw new Error(data.message || 'Gagal submit')
      }
    }
  } catch (err) {
    console.error('Submit error details:', err)
    error.value = 'Gagal mengajukan pengambilan'
    errorDetail.value = err.message || 'Terjadi kesalahan'

    if (err.message.includes('NetworkError') || err.message.includes('Failed to fetch')) {
      errorDetail.value = 'Koneksi ke server terputus'
    } else {
      errorDetail.value = err.message
    }
  } finally {
    submitting.value = false
  }
}

// Fungsi test koneksi

// Initialize
const initForm = async () => {
  loading.value = true
  error.value = ''
  errorDetail.value = ''

  try {
    await Promise.all([fetchJadwalData(), fetchWargaData()])
  } catch (err) {
    console.error('Init error:', err)
    error.value = 'Gagal memuat data form'
    errorDetail.value = err.message
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  initForm()
})
</script>

<style scoped>
.text-dark-green {
  color: #08602e !important;
}

/* Form Card */
.form-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Jadwal Info */
.jadwal-info {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.info-item {
  padding: 8px 0;
}

/* Jenis Sampah Cards */
.jenis-card {
  border: 2px solid transparent;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.jenis-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.jenis-card.selected {
  border-color: #1976d2;
  background-color: rgba(25, 118, 210, 0.05);
}

/* Upload Area */
.upload-area {
  border: 2px dashed #ced4da;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #1976d2;
  background-color: rgba(25, 118, 210, 0.05);
}

/* Photo Preview */
.photo-preview {
  position: relative;
  display: inline-block;
}

.remove-photo {
  position: absolute;
  top: -8px;
  right: -8px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Info Card */
.info-card {
  border-radius: 12px;
  border-left: 4px solid #08602e;
  background: #f8fff9;
}

.info-list {
  padding-left: 20px;
  margin: 0;
}

.info-list li {
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: #555;
}

/* Success Dialog */
.success-dialog {
  border-radius: 20px;
  min-width: 320px;
  max-width: 400px;
}
.warga-info {
  border: 1px solid #b3e0ff;
  background-color: #e6f7ff;
}
</style>
