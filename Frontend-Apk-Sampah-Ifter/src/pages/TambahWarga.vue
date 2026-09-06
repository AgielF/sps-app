<template>
  <q-page class="q-pa-md bg-green-1">
    <div class="row items-center q-mb-md">
      <q-btn flat round icon="arrow_back" @click="goBack" />
      <div class="text-h6 q-ml-md text-weight-bold text-dark">
        {{ isEdit ? 'Edit Warga' : 'Tambah Warga Baru' }}
      </div>
    </div>

    <q-form @submit="onSubmit" class="q-gutter-y-md">
      <q-card class="form-card">
        <q-card-section>
          <div class="text-subtitle1 text-weight-bold q-mb-sm">Informasi Akun</div>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.username"
                label="Username"
                outlined
                dense
                :rules="[(val) => !!val || 'Username wajib diisi']"
              />
            </div>
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.email"
                label="Email"
                type="email"
                outlined
                dense
                :rules="[
                  (val) => !!val || 'Email wajib diisi',
                  (val) => /.+@.+\..+/.test(val) || 'Email tidak valid',
                ]"
              />
            </div>
          </div>

          <div class="row q-col-gutter-md q-mt-sm">
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                :label="isEdit ? 'Password Baru (Opsional)' : 'Password'"
                outlined
                dense
                :hint="
                  isEdit ? 'Kosongkan jika tidak ingin mengubah password' : 'Minimal 6 karakter'
                "
                :rules="[(val) => !val || val.length >= 6 || 'Password minimal 6 karakter']"
              >
                <template v-slot:append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.nama_lengkap"
                label="Nama Lengkap"
                outlined
                dense
                :rules="[(val) => !!val || 'Nama lengkap wajib diisi']"
              />
            </div>
          </div>

          <!-- Konfirmasi Password hanya jika mengisi password baru di mode edit -->
          <div v-if="isEdit && form.password" class="row q-col-gutter-md q-mt-sm">
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                label="Konfirmasi Password Baru"
                outlined
                dense
                :rules="[
                  (val) => !!val || 'Harap konfirmasi password baru',
                  (val) => val === form.password || 'Password tidak cocok',
                ]"
              >
                <template v-slot:append>
                  <q-icon
                    :name="showConfirmPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="showConfirmPassword = !showConfirmPassword"
                  />
                </template>
              </q-input>
            </div>
          </div>

          <div class="text-subtitle1 text-weight-bold q-mt-lg q-mb-sm">Data Pribadi</div>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.nik"
                label="NIK"
                outlined
                dense
                mask="################"
                :rules="[(val) => !val || val.length === 16 || 'NIK harus 16 digit']"
              />
            </div>
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.no_telepon"
                label="No. Telepon"
                outlined
                dense
                mask="##############"
              />
            </div>
          </div>

          <div class="row q-col-gutter-md q-mt-sm">
            <div class="col-12 col-md-6">
              <q-input v-model="form.rt" label="RT" outlined dense mask="##" />
            </div>
            <div class="col-12 col-md-6">
              <q-input v-model="form.rw" label="RW" outlined dense mask="##" />
            </div>
          </div>

          <div class="q-mt-sm">
            <q-input
              v-model="form.alamat_lengkap"
              label="Alamat Lengkap"
              outlined
              dense
              type="textarea"
              rows="2"
            />
          </div>

          <div class="q-mt-sm">
            <q-input
              v-model="form.kelurahan"
              label="Kelurahan"
              outlined
              dense
              readonly
              bg-color="grey-2"
            />
          </div>

          <div v-if="isEdit" class="q-mt-sm">
            <q-input
              v-model.number="form.saldo"
              label="Saldo"
              type="number"
              outlined
              dense
              prefix="Rp"
              :rules="[(val) => val >= 0 || 'Saldo tidak boleh negatif']"
            />
          </div>

          <div class="text-subtitle1 text-weight-bold q-mt-lg q-mb-sm">Lokasi (Pilih di Peta)</div>

          <!-- Map Container -->
          <div class="q-mb-md">
            <div class="row items-center q-mb-sm">
              <div class="col">
                <div class="text-caption text-grey-7">
                  <q-icon name="location_on" color="primary" size="sm" class="q-mr-xs" />
                  Klik pada peta untuk menentukan lokasi atau drag marker
                </div>
              </div>
              <div class="col-auto">
                <q-btn
                  label="Lokasi Saya"
                  color="primary"
                  outline
                  dense
                  size="sm"
                  @click="getCurrentLocation"
                  :loading="gettingLocation"
                />
              </div>
            </div>

            <!-- Leaflet Map -->
            <div class="map-container" ref="mapContainer">
              <!-- Vue Leaflet akan di-mount di sini -->
            </div>

            <!-- Koordinat Display -->
            <div class="row q-col-gutter-sm q-mt-sm">
              <div class="col-6">
                <q-input
                  v-model="form.latitude"
                  label="Latitude"
                  outlined
                  dense
                  readonly
                  bg-color="grey-2"
                >
                  <template v-slot:append>
                    <q-icon
                      name="content_copy"
                      class="cursor-pointer"
                      @click="copyToClipboard(form.latitude)"
                    />
                  </template>
                </q-input>
              </div>
              <div class="col-6">
                <q-input
                  v-model="form.longitude"
                  label="Longitude"
                  outlined
                  dense
                  readonly
                  bg-color="grey-2"
                >
                  <template v-slot:append>
                    <q-icon
                      name="content_copy"
                      class="cursor-pointer"
                      @click="copyToClipboard(form.longitude)"
                    />
                  </template>
                </q-input>
              </div>
            </div>

            <div class="text-caption text-grey-7 q-mt-xs">
              <q-icon name="info" size="xs" class="q-mr-xs" />
              Latitude: {{ form.latitude || '-' }}, Longitude: {{ form.longitude || '-' }}
            </div>
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix untuk icon Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

const route = useRoute()
const router = useRouter()
const $q = useQuasar()

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const isEdit = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const gettingLocation = ref(false)

// Leaflet refs
const mapContainer = ref(null)
let map = null
let marker = null

// Default lokasi Suraja
const DEFAULT_LAT = -7.09521
const DEFAULT_LNG = 107.484
const DEFAULT_ZOOM = 15

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '', // Hanya untuk konfirmasi saat edit
  nama_lengkap: '',
  nik: '',
  no_telepon: '',
  alamat_lengkap: '',
  rt: '',
  rw: '',
  kelurahan: 'Suraja',
  latitude: null,
  longitude: null,
  saldo: 0,
})

// Initialize map
const initMap = () => {
  if (!mapContainer.value) return

  // Destroy existing map
  if (map) {
    map.remove()
  }

  // Create new map
  map = L.map(mapContainer.value).setView([DEFAULT_LAT, DEFAULT_LNG], DEFAULT_ZOOM)

  // Add tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)

  // Create marker
  const initialLat = form.value.latitude || DEFAULT_LAT
  const initialLng = form.value.longitude || DEFAULT_LNG

  marker = L.marker([initialLat, initialLng], {
    draggable: true,
  }).addTo(map)

  // Update form when marker is moved
  marker.on('dragend', function () {
    const position = marker.getLatLng()
    form.value.latitude = position.lat.toFixed(6)
    form.value.longitude = position.lng.toFixed(6)
  })

  // Update marker when clicking on map
  map.on('click', function (event) {
    const { lat, lng } = event.latlng
    marker.setLatLng([lat, lng])
    form.value.latitude = lat.toFixed(6)
    form.value.longitude = lng.toFixed(6)
  })

  // Fit map to container
  setTimeout(() => {
    map.invalidateSize()
  }, 100)
}

// Get current location
const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    $q.notify({
      type: 'warning',
      message: 'Geolocation tidak didukung oleh browser',
      position: 'top',
    })
    return
  }

  gettingLocation.value = true

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude

      // Update form
      form.value.latitude = lat.toFixed(6)
      form.value.longitude = lng.toFixed(6)

      // Update map and marker
      map.setView([lat, lng], 17)
      marker.setLatLng([lat, lng])

      gettingLocation.value = false

      $q.notify({
        type: 'positive',
        message: 'Lokasi berhasil didapatkan',
        position: 'top',
        timeout: 2000,
      })
    },
    (error) => {
      console.error('Geolocation error:', error)
      gettingLocation.value = false

      let errorMessage = 'Gagal mendapatkan lokasi'
      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMessage = 'Izin lokasi ditolak. Izinkan akses lokasi di browser.'
          break
        case error.POSITION_UNAVAILABLE:
          errorMessage = 'Informasi lokasi tidak tersedia'
          break
        case error.TIMEOUT:
          errorMessage = 'Permintaan lokasi timeout'
          break
      }

      $q.notify({
        type: 'negative',
        message: errorMessage,
        position: 'top',
        timeout: 4000,
      })
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0,
    },
  )
}

// Copy to clipboard
const copyToClipboard = (text) => {
  if (!text) return

  navigator.clipboard.writeText(text).then(() => {
    $q.notify({
      type: 'info',
      message: 'Koordinat disalin ke clipboard',
      position: 'top',
      timeout: 2000,
    })
  })
}

// Load data for edit
onMounted(async () => {
  console.log('TambahWarga mounted, route params:', route.params)

  if (route.params.id) {
    isEdit.value = true
    console.log('Edit mode for ID:', route.params.id)
    await loadWargaData(route.params.id)
  }

  // Initialize map after component is mounted
  nextTick(() => {
    initMap()
  })
})

// Cleanup on unmount
onUnmounted(() => {
  if (map) {
    map.remove()
  }
})

async function loadWargaData(id) {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await axios.get(`${API_URL}/api/warga/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    console.log('Loaded warga data:', response.data)

    if (response.data.success) {
      const data = response.data.data
      form.value = {
        username: data.username || '',
        email: data.email || '',
        password: '', // Kosongkan - biarkan user pilih mau ubah atau tidak
        confirmPassword: '', // Kosongkan konfirmasi
        nama_lengkap: data.nama_lengkap || data.nama_warga || '',
        nik: data.nik || '',
        no_telepon: data.no_telepon || data.no_telp || '',
        alamat_lengkap: data.alamat_lengkap || data.alamat || '',
        rt: data.rt || '',
        rw: data.rw || '',
        kelurahan: data.kelurahan || 'Suraja',
        latitude: data.latitude ? data.latitude.toString() : null,
        longitude: data.longitude ? data.longitude.toString() : null,
        saldo: data.saldo || 0,
      }

      console.log('Form after load:', form.value)

      // Update map if coordinates exist
      if (data.latitude && data.longitude) {
        nextTick(() => {
          if (map && marker) {
            const lat = parseFloat(data.latitude)
            const lng = parseFloat(data.longitude)
            map.setView([lat, lng], 17)
            marker.setLatLng([lat, lng])

            // Juga update form dengan koordinat yang sudah diformat
            form.value.latitude = lat.toFixed(6)
            form.value.longitude = lng.toFixed(6)
          }
        })
      }
    }
  } catch (error) {
    console.error('Error loading warga:', error)

    if (error.response?.status === 401) {
      $q.notify({
        type: 'negative',
        message: 'Sesi telah berakhir. Silakan login kembali.',
        position: 'top',
      })
      router.push('/login')
      return
    }

    $q.notify({
      type: 'negative',
      message: error.response?.data?.message || 'Gagal memuat data warga',
      position: 'top',
    })
  } finally {
    loading.value = false
  }
}

async function onSubmit() {
  console.log('Submitting form...')

  // Validasi dasar
  if (!form.value.username || !form.value.email || !form.value.nama_lengkap) {
    $q.notify({
      type: 'warning',
      message: 'Username, Email, dan Nama Lengkap wajib diisi',
      position: 'top',
    })
    return
  }

  // **PERBAIKAN DI SINI**: Validasi password untuk create (handle di sini, bukan di rules)
  if (!isEdit.value) {
    if (!form.value.password || form.value.password.length < 6) {
      $q.notify({
        type: 'warning',
        message: 'Password wajib diisi dan minimal 6 karakter untuk warga baru',
        position: 'top',
      })
      return
    }
  }

  // Validasi password untuk edit - hanya jika diisi
  if (isEdit.value && form.value.password) {
    if (form.value.password.length < 6) {
      $q.notify({
        type: 'warning',
        message: 'Password baru minimal 6 karakter',
        position: 'top',
      })
      return
    }

    // Konfirmasi password hanya diperlukan jika password diisi
    if (form.value.password !== form.value.confirmPassword) {
      $q.notify({
        type: 'warning',
        message: 'Password baru dan konfirmasi tidak cocok',
        position: 'top',
      })
      return
    }
  }

  // Validasi koordinat
  if (!form.value.latitude || !form.value.longitude) {
    $q.notify({
      type: 'warning',
      message: 'Silakan pilih lokasi di peta terlebih dahulu',
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

    const url = isEdit.value ? `${API_URL}/api/warga/${route.params.id}` : `${API_URL}/api/warga/`
    const method = isEdit.value ? 'PUT' : 'POST'

    // Siapkan data untuk dikirim
    const dataToSend = {
      username: form.value.username,
      email: form.value.email,
      nama_lengkap: form.value.nama_lengkap,
      nik: form.value.nik,
      no_telepon: form.value.no_telepon,
      alamat_lengkap: form.value.alamat_lengkap,
      rt: form.value.rt,
      rw: form.value.rw,
      kelurahan: form.value.kelurahan,
      latitude: parseFloat(form.value.latitude),
      longitude: parseFloat(form.value.longitude),
      saldo: isEdit.value ? parseFloat(form.value.saldo) : 0,
    }

    // Handle password
    if (!isEdit.value) {
      // Untuk create - password wajib
      dataToSend.password = form.value.password
    } else if (form.value.password && form.value.password.trim() !== '') {
      // Untuk edit - hanya kirim password jika diisi
      dataToSend.password = form.value.password
    }
    // Jika edit tanpa password baru, jangan kirim field password sama sekali

    // Handle RT/RW format
    if (dataToSend.rt && dataToSend.rt.length === 1) {
      dataToSend.rt = '0' + dataToSend.rt
    }
    if (dataToSend.rw && dataToSend.rw.length === 1) {
      dataToSend.rw = '0' + dataToSend.rw
    }

    // Debug log
    console.log('Data to send:', dataToSend)
    console.log('URL:', url)
    console.log('Method:', method)

    const response = await axios({
      method,
      url,
      data: dataToSend,
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    console.log('Response:', response.data)

    if (response.data.success) {
      $q.notify({
        type: 'positive',
        message:
          response.data.message ||
          (isEdit.value ? 'Data warga berhasil diupdate!' : 'Warga baru berhasil ditambahkan!'),
        position: 'top',
        timeout: 3000,
      })

      setTimeout(() => {
        router.push('/admin/data/warga')
      }, 1000)
    } else {
      $q.notify({
        type: 'warning',
        message: response.data.message || 'Operasi berhasil tetapi tidak ada pesan konfirmasi',
        position: 'top',
      })
    }
  } catch (error) {
    console.error('Error saving warga:', error)
    console.error('Error response:', error.response?.data)

    if (error.response?.status === 401) {
      $q.notify({
        type: 'negative',
        message: 'Sesi telah berakhir. Silakan login kembali.',
        position: 'top',
      })
      router.push('/login')
      return
    }

    let errorMessage = 'Terjadi kesalahan saat menyimpan data'
    if (error.response?.data?.message) {
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
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/admin/data/warga')
  }
}
</script>

<style scoped>
.form-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.map-container {
  height: 300px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #e0e0e0;
}

/* Leaflet map fixes */
:deep(.leaflet-container) {
  font-family: inherit;
}

:deep(.leaflet-control-zoom) {
  border: none !important;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

:deep(.leaflet-control-zoom a) {
  background-color: white;
  color: #333;
  border-radius: 4px;
  margin: 2px;
}

:deep(.leaflet-control-zoom a:hover) {
  background-color: #f5f5f5;
}
</style>
