<template>
  <q-page class="q-pa-md bg-green-1">
    <div class="row items-center q-mb-md">
      <q-btn flat round icon="arrow_back" @click="goBack" />
      <div class="text-h6 q-ml-md text-weight-bold text-dark">
        {{ isEdit ? 'Edit Petugas' : 'Tambah Petugas Baru' }}
      </div>
    </div>

    <q-form @submit="onSubmit" class="q-gutter-y-md">
      <q-card class="form-card">
        <q-card-section>
          <div class="text-subtitle1 text-weight-bold q-mb-sm">Informasi Akun</div>

          <q-input
            v-model="form.username"
            label="Username *"
            outlined
            dense
            :rules="[(val) => !!val || 'Username wajib diisi']"
          />

          <q-input
            v-model="form.email"
            label="Email *"
            type="email"
            outlined
            dense
            :rules="[
              (val) => !!val || 'Email wajib diisi',
              (val) => /.+@.+\..+/.test(val) || 'Email tidak valid',
            ]"
          />

          <div v-if="isEdit" class="q-mb-sm">
            <div class="text-caption text-grey-7 q-mb-xs">
              <q-icon name="lock" color="blue" size="sm" class="q-mr-xs" />
              Password saat ini tidak dapat ditampilkan (tersimpan terenkripsi)
            </div>
          </div>

          <q-input
            v-model="form.password"
            :label="isEdit ? 'Password Baru (kosongkan jika tidak diubah)' : 'Password *'"
            :type="showPassword ? 'text' : 'password'"
            outlined
            dense
            :hint="isEdit ? 'Minimal 6 karakter jika ingin mengubah' : 'Minimal 6 karakter'"
            :rules="isEdit ? [] : [(val) => (!!val && val.length >= 6) || 'Minimal 6 karakter']"
          >
            <template v-slot:append>
              <q-icon
                :name="showPassword ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="showPassword = !showPassword"
              />
            </template>
          </q-input>

          <!-- Tombol Reset Password -->
          <div v-if="isEdit" class="q-mt-md">
            <q-btn
              label="Reset Password ke Default"
              color="orange"
              outline
              dense
              @click="resetPassword"
              class="full-width"
            />
            <div class="text-caption text-grey-7 q-mt-xs">
              Password akan direset ke: <strong>password123</strong>
            </div>
          </div>

          <div class="text-subtitle1 text-weight-bold q-mt-lg q-mb-sm">Informasi Pribadi</div>

          <q-input
            v-model="form.nama_lengkap"
            label="Nama Lengkap *"
            outlined
            dense
            :rules="[(val) => !!val || 'Nama wajib diisi']"
          />

          <q-input
            v-model="form.nik"
            label="NIK (16 digit)"
            outlined
            dense
            mask="################"
            unmasked-value
            :rules="[(val) => !val || val.length === 16 || 'NIK harus 16 digit']"
          />

          <q-input
            v-model="form.no_telepon"
            label="Nomor Telepon"
            outlined
            dense
            mask="##############"
            unmasked-value
          />

          <q-input v-model="form.alamat" label="Alamat" type="textarea" outlined dense rows="2" />

          <q-select
            v-model="form.status_kerja"
            label="Status Kerja"
            :options="statusOptions"
            outlined
            dense
            emit-value
            map-options
          />
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const $q = useQuasar()

const API_URL = 'http://127.0.0.1:5000'

const isEdit = ref(false)
const loading = ref(false)
const showPassword = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  nama_lengkap: '',
  nik: '',
  no_telepon: '',
  alamat: '',
  status_kerja: 'aktif',
  gaji_per_karung: 5000,
})

const statusOptions = [
  { label: 'Aktif', value: 'aktif' },
  { label: 'Cuti', value: 'cuti' },
  { label: 'Resign', value: 'resign' },
]

// Load data for edit
onMounted(() => {
  if (route.params.id) {
    isEdit.value = true
    loadPetugasData(route.params.id)
  }
})

async function loadPetugasData(id) {
  loading.value = true
  try {
    const response = await axios.get(`${API_URL}/api/petugas/${id}`, {
      headers: getAuthHeader(),
    })

    if (response.data.success) {
      const data = response.data.data
      form.value = {
        username: data.username,
        email: data.email,
        password: '********', // Tampilkan placeholder, bukan kosong
        nama_lengkap: data.nama_lengkap,
        nik: data.nik || '',
        no_telepon: data.no_telepon || '',
        alamat: data.alamat || '',
        status_kerja: data.status_kerja,
        gaji_per_karung: data.gaji_per_karung || 5000,
      }
      console.log('✅ Loaded petugas data')
    }
  } catch (error) {
    console.error('Error loading petugas:', error)
    $q.notify({
      type: 'negative',
      message: 'Gagal memuat data petugas',
    })
  } finally {
    loading.value = false
  }
}

async function onSubmit() {
  loading.value = true

  try {
    const url = isEdit.value
      ? `${API_URL}/api/petugas/${route.params.id}`
      : `${API_URL}/api/petugas/`

    const method = isEdit.value ? 'PUT' : 'POST'

    // Siapkan data untuk dikirim
    const dataToSend = { ...form.value }

    // Untuk edit mode: handle password logic
    if (isEdit.value) {
      // Jika password masih placeholder atau kosong, jangan kirim
      if (dataToSend.password === '********' || dataToSend.password.trim() === '') {
        console.log('🗑️ Password tidak diubah, menghapus dari request')
        delete dataToSend.password
      } else {
        console.log('🔄 Password diubah, mengirim password baru')
      }
    }

    // Untuk create, password wajib
    if (!isEdit.value && (!dataToSend.password || dataToSend.password.length < 6)) {
      $q.notify({
        type: 'negative',
        message: 'Password minimal 6 karakter untuk petugas baru',
        position: 'top',
      })
      loading.value = false
      return
    }

    console.log('📤 Data yang dikirim:', dataToSend)

    const response = await axios({
      method,
      url,
      data: dataToSend,
      headers: getAuthHeader(),
    })

    if (response.data.success) {
      $q.notify({
        type: 'positive',
        message: response.data.message,
        position: 'top',
        timeout: 2000,
      })

      setTimeout(() => {
        router.push('/admin/data/petugas')
      }, 500)
    }
  } catch (error) {
    console.error('Error saving petugas:', error)

    let errorMessage = 'Terjadi kesalahan'
    if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.response?.data?.errors) {
      errorMessage = Array.isArray(error.response.data.errors)
        ? error.response.data.errors.join(', ')
        : error.response.data.errors
    }

    $q.notify({
      type: 'negative',
      message: errorMessage,
      position: 'top',
    })
  } finally {
    loading.value = false
  }
}

// Helper untuk get auth header
const getAuthHeader = () => {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

function goBack() {
  router.back()
}

const resetPassword = () => {
  $q.dialog({
    title: 'Reset Password',
    message: 'Yakin reset password ke default (password123)?',
    cancel: true,
    persistent: true,
  }).onOk(() => {
    form.value.password = 'password123'
    $q.notify({
      type: 'info',
      message: 'Password direset ke default. Klik Simpan untuk update.',
      position: 'top',
    })
  })
}
</script>

<style scoped>
.form-card {
  border-radius: 16px;
}
</style>
