<template>
  <q-page class="q-pa-md bg-grey-1">
    <!-- Header -->
    <div class="row items-center q-mb-md">
      <div class="col">
        <div class="text-h6 text-weight-bold">Penggajian Petugas</div>
        <div class="text-caption text-grey-7">Kelola gaji berdasarkan jadwal</div>
      </div>
      <div class="col-auto">
        <q-btn label="Tambah Penggajian" color="primary" icon="paid" @click="showFormGaji" />
      </div>
    </div>

    <!-- STEP 1: PILIH JADWAL -->
    <div v-if="step === 1">
      <div class="text-h6 q-mb-md">Pilih Jadwal</div>

      <!-- Loading State -->
      <div v-if="loadingJadwal" class="text-center q-py-lg">
        <q-spinner color="primary" size="2em" />
        <div class="text-caption q-mt-sm">Memuat data jadwal...</div>
      </div>

      <!-- No Data -->
      <div v-else-if="jadwalList.length === 0" class="text-center q-py-xl bg-white rounded-borders">
        <q-icon name="search_off" size="4em" color="grey-4" />
        <div class="text-h6 text-grey-7 q-mt-md">Tidak ada jadwal ditemukan</div>
        <q-btn label="Refresh" color="primary" outline @click="loadJadwal" class="q-mt-md" />
      </div>

      <!-- List Jadwal -->
      <div v-else>
        <div class="text-positive q-mb-sm">✅ Ditemukan {{ jadwalList.length }} jadwal</div>

        <div class="row q-col-gutter-md">
          <div v-for="jadwal in jadwalList" :key="jadwal.id" class="col-12 col-md-6">
            <q-card
              class="cursor-pointer shadow-1 hover-shadow-3"
              @click="pilihJadwal(jadwal)"
              flat
              bordered
            >
              <q-card-section>
                <div class="row items-center">
                  <div class="col">
                    <div class="text-subtitle1 text-weight-bold">
                      {{ jadwal.wilayah }}
                    </div>

                    <div class="text-caption text-grey-7 q-mt-xs">
                      <q-icon name="event" size="xs" class="q-mr-xs" />
                      <strong>Tanggal:</strong> {{ jadwal.tanggal || 'Tidak ada' }}
                    </div>

                    <div class="text-caption text-grey-7">
                      <q-icon name="schedule" size="xs" class="q-mr-xs" />
                      <strong>Jam:</strong> {{ jadwal.jam_mulai || '--' }} -
                      {{ jadwal.jam_selesai || '--' }}
                    </div>

                    <div v-if="jadwal.keterangan" class="text-caption text-grey-7 q-mt-xs">
                      <q-icon name="info" size="xs" class="q-mr-xs" />
                      {{ jadwal.keterangan }}
                    </div>
                  </div>

                  <div class="col-auto">
                    <q-btn icon="arrow_forward" color="primary" flat round />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>

    <!-- STEP 2: INPUT GAJI -->
    <div v-if="step === 2">
      <!-- Header dengan tombol kembali -->
      <div class="row items-center q-mb-md">
        <q-btn icon="arrow_back" flat @click="kembaliKeJadwal" />
        <div class="text-h6">Input Gaji untuk {{ jadwalDetail.wilayah || 'Jadwal' }}</div>
      </div>

      <!-- Info Jadwal -->
      <q-card class="q-mb-md bg-blue-1">
        <q-card-section>
          <div class="row items-center">
            <div class="col">
              <div class="text-weight-bold text-h6">{{ jadwalDetail.wilayah }}</div>
              <div class="text-caption">
                <q-icon name="event" size="xs" /> {{ jadwalDetail.tanggal }}
              </div>
              <div v-if="jadwalDetail.keterangan" class="text-caption q-mt-xs">
                {{ jadwalDetail.keterangan }}
              </div>
            </div>
            <div class="col-auto">
              <q-badge color="green" v-if="petugasList.length > 0">
                {{ petugasList.length }} petugas
              </q-badge>
              <q-badge color="orange" v-else> Tidak ada petugas </q-badge>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Form Tanggal & Keterangan -->
      <q-card class="q-mb-md">
        <q-card-section>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.tanggal_bayar"
                label="Tanggal Pembayaran"
                outlined
                type="date"
                :rules="[(val) => !!val || 'Tanggal wajib diisi']"
              />
            </div>
            <div class="col-12 col-md-6">
              <q-input
                v-model="form.keterangan_umum"
                label="Keterangan Umum"
                outlined
                placeholder="Contoh: Gaji Bulan Desember"
              />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Daftar Petugas -->
      <q-card>
        <q-card-section>
          <div class="text-subtitle1 q-mb-md">Daftar Petugas</div>

          <!-- Loading Petugas -->
          <div v-if="loadingPetugas" class="text-center q-py-lg">
            <q-spinner color="primary" size="1.5em" />
            <div class="text-caption q-mt-sm">Memuat data petugas...</div>
          </div>

          <!-- No Petugas -->
          <div v-else-if="petugasList.length === 0" class="text-center q-py-lg text-grey-7">
            <q-icon name="people_outline" size="3em" class="q-mb-sm" />
            <div>Tidak ada petugas di jadwal ini</div>
            <div class="text-caption q-mt-sm">Pastikan petugas sudah ditugaskan ke jadwal ini</div>
          </div>

          <!-- Tabel Input Gaji -->
          <div v-else>
            <div class="table-responsive">
              <table class="q-table" style="width: 100%">
                <thead>
                  <tr class="bg-grey-3">
                    <th class="text-left">Nama Petugas</th>
                    <th class="text-center">NIK</th>
                    <th class="text-center">Gaji (Rp)</th>
                    <th class="text-left">Keterangan</th>
                    <th class="text-center">Status Kehadiran</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="petugas in petugasList" :key="petugas.id">
                    <td>
                      <div class="text-weight-medium">{{ petugas.nama_lengkap }}</div>
                      <div class="text-caption text-grey-7">{{ petugas.no_telepon }}</div>
                    </td>
                    <td class="text-center">
                      {{ petugas.nik || '-' }}
                    </td>
                    <td class="text-center">
                      <q-input
                        v-model.number="gajiItems[petugas.id]"
                        type="number"
                        dense
                        outlined
                        placeholder="0"
                        style="min-width: 150px"
                        :rules="[(val) => val > 0 || 'Harus lebih dari 0']"
                      >
                        <template v-slot:prepend>
                          <span class="text-caption">Rp</span>
                        </template>
                      </q-input>
                    </td>
                    <td>
                      <q-input
                        v-model="keteranganItems[petugas.id]"
                        type="text"
                        dense
                        outlined
                        placeholder="Opsional"
                        style="min-width: 200px"
                      />
                    </td>
                    <td class="text-center">
                      <q-badge :color="getStatusColor(petugas.status_kehadiran)">
                        {{ petugas.status_kehadiran || 'hadir' }}
                      </q-badge>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Total & Tombol Simpan -->
            <div class="row items-center q-mt-lg q-pa-md bg-green-1 rounded-borders">
              <div class="col">
                <div class="text-h5 text-weight-bold text-primary">
                  Total: {{ formatCurrency(totalGaji) }}
                </div>
                <div class="text-caption text-grey-7">{{ petugasList.length }} petugas</div>
              </div>
              <div class="col-auto">
                <q-btn
                  label="Hitung Otomatis"
                  color="secondary"
                  icon="calculate"
                  @click="hitungGajiOtomatis"
                  class="q-mr-sm"
                  :disable="saving"
                />
                <q-btn
                  label="Simpan Gaji"
                  color="primary"
                  icon="save"
                  @click="simpanGaji"
                  :loading="saving"
                  :disable="totalGaji <= 0 || saving"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- RIWAYAT GAJI -->
    <div class="q-mt-xl" v-if="step === 1">
      <div class="text-h6 q-mb-md">Riwayat Penggajian</div>

      <q-card>
        <q-card-section>
          <div v-if="riwayatGaji.length === 0" class="text-center q-py-lg text-grey-7">
            <q-icon name="history" size="3em" class="q-mb-sm" />
            <div>Belum ada riwayat penggajian</div>
          </div>

          <div v-else>
            <div class="row q-col-gutter-md">
              <div v-for="gaji in riwayatGaji.slice(0, 6)" :key="gaji.id" class="col-12 col-md-6">
                <q-card flat bordered class="hover-shadow-2">
                  <q-card-section>
                    <div class="row items-center">
                      <div class="col">
                        <div class="text-weight-bold">{{ gaji.nama_lengkap }}</div>
                        <div class="text-caption text-grey-7">
                          {{ gaji.tanggal_bayar }} | {{ gaji.periode }}
                        </div>
                        <div class="text-caption">{{ gaji.wilayah }}</div>
                        <div v-if="gaji.keterangan" class="text-caption text-grey-7 q-mt-xs">
                          {{ gaji.keterangan }}
                        </div>
                      </div>
                      <div class="col-auto">
                        <div class="text-h6 text-red text-weight-bold">
                          {{ formatCurrency(gaji.gaji) }}
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
            <div class="text-center q-mt-md">
              <q-btn label="Lihat Semua Riwayat" color="primary" flat />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import axios from 'axios'

const $q = useQuasar()
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

// States
const loadingJadwal = ref(false)
const loadingPetugas = ref(false)
const saving = ref(false)
const step = ref(1)
const jadwalList = ref([])
const selectedJadwalId = ref(null)
const jadwalDetail = ref({})
const petugasList = ref([])
const riwayatGaji = ref([])

// Forms
const form = ref({
  tanggal_bayar: new Date().toISOString().split('T')[0],
  keterangan_umum: '',
})

const gajiItems = ref({})
const keteranganItems = ref({})

// Computed
const totalGaji = computed(() => {
  return Object.values(gajiItems.value).reduce((sum, val) => {
    return sum + (Number(val) || 0)
  }, 0)
})

// Helper Functions
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
  }).format(amount || 0)
}

const getStatusColor = (status) => {
  const colors = {
    hadir: 'green',
    izin: 'blue',
    sakit: 'orange',
    alpha: 'red',
  }
  return colors[status] || 'grey'
}

// Methods
const showFormGaji = () => {
  step.value = 1
  loadJadwal()
}

const loadJadwal = async () => {
  loadingJadwal.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${API_URL}/api/gaji/jadwal`, {
      headers: { Authorization: `Bearer ${token}` },
      timeout: 8000,
    })

    if (res.data.success && Array.isArray(res.data.data)) {
      jadwalList.value = res.data.data
      if (res.data.data.length > 0) {
        $q.notify({
          type: 'positive',
          message: `Memuat ${res.data.data.length} jadwal`,
          timeout: 1500,
        })
      }
    } else {
      jadwalList.value = []
    }
  } catch (error) {
    console.error('Error loading jadwal:', error)
    jadwalList.value = []
    $q.notify({
      type: 'negative',
      message: 'Gagal memuat data jadwal',
      caption: error.message,
    })
  } finally {
    loadingJadwal.value = false
  }
}

const pilihJadwal = async (jadwal) => {
  console.log('🎯 Selected jadwal:', jadwal)

  selectedJadwalId.value = jadwal.id
  jadwalDetail.value = jadwal
  step.value = 2

  loadingPetugas.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${API_URL}/api/gaji/jadwal/${jadwal.id}/petugas`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    console.log('👥 Petugas response:', res.data)

    if (res.data.success) {
      if (res.data.data.jadwal) {
        jadwalDetail.value = res.data.data.jadwal
      }

      petugasList.value = res.data.data.petugas || []
      console.log('👥 Petugas loaded:', petugasList.value.length, 'orang')

      // Reset gaji forms
      gajiItems.value = {}
      keteranganItems.value = {}

      // Set default keterangan
      if (!form.value.keterangan_umum) {
        form.value.keterangan_umum = `Gaji jadwal ${jadwalDetail.value.wilayah} - ${jadwalDetail.value.tanggal}`
      }

      // Cek apakah sudah ada data gaji sebelumnya
      const cekRes = await axios.get(`${API_URL}/api/gaji/jadwal/${jadwal.id}/cek`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (cekRes.data.success && cekRes.data.sudah_ada) {
        // Isi otomatis jika sudah ada
        cekRes.data.data.forEach((item) => {
          gajiItems.value[item.petugas_id] = item.gaji
          keteranganItems.value[item.petugas_id] = item.keterangan || ''
        })

        $q.notify({
          type: 'info',
          message: 'Data gaji sebelumnya ditemukan',
          caption: 'Silahkan edit jika perlu',
          timeout: 3000,
        })
      }
    }
  } catch (error) {
    console.error('❌ Error loading petugas:', error)
    $q.notify({
      type: 'negative',
      message: 'Gagal memuat data petugas',
      caption: error.message,
    })
  } finally {
    loadingPetugas.value = false
  }
}

const kembaliKeJadwal = () => {
  step.value = 1
  selectedJadwalId.value = null
  petugasList.value = []
  gajiItems.value = {}
  keteranganItems.value = {}
}

const hitungGajiOtomatis = () => {
  // Hitung gaji berdasarkan gaji_per_karung atau aturan lainnya
  petugasList.value.forEach((petugas) => {
    if (petugas.gaji_per_karung && petugas.gaji_per_karung > 0) {
      // Contoh: gaji = gaji_per_karung * 10 (asumsi 10 karung)
      gajiItems.value[petugas.id] = petugas.gaji_per_karung * 10
    } else {
      // Atau berikan gaji default
      gajiItems.value[petugas.id] = 100000
    }

    // Set keterangan default jika kosong
    if (!keteranganItems.value[petugas.id]) {
      keteranganItems.value[petugas.id] = `Gaji ${jadwalDetail.value.wilayah}`
    }
  })

  $q.notify({
    type: 'info',
    message: 'Gaji dihitung otomatis',
    timeout: 2000,
  })
}

const simpanGaji = async () => {
  console.log('💾 simpanGaji START')

  // Validasi
  const items = []
  for (const petugas of petugasList.value) {
    const gaji = gajiItems.value[petugas.id]
    if (!gaji || gaji <= 0) {
      $q.notify({
        type: 'warning',
        message: `Gaji untuk ${petugas.nama_lengkap} belum diisi`,
      })
      return
    }
    items.push({
      petugas_id: petugas.id,
      gaji: gaji,
      keterangan: keteranganItems.value[petugas.id] || '',
    })
  }

  if (items.length === 0) {
    $q.notify({ type: 'warning', message: 'Tidak ada data gaji yang valid' })
    return
  }

  saving.value = true
  try {
    const token = localStorage.getItem('token')
    const payload = {
      tanggal_bayar: form.value.tanggal_bayar,
      jadwal_id: selectedJadwalId.value,
      items: items,
      keterangan_umum: form.value.keterangan_umum || `Gaji jadwal ${jadwalDetail.value.wilayah}`,
    }

    console.log('💾 Payload:', payload)

    // Pakai endpoint /simpan yang baru
    const res = await axios.post(`${API_URL}/api/gaji/simpan`, payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    console.log('✅ Save response:', res.data)

    if (res.data.success) {
      $q.notify({
        type: 'positive',
        message: `✅ Gaji berhasil disimpan!`,
        caption: `Total: ${formatCurrency(res.data.data.total_gaji)} untuk ${res.data.data.petugas_count} petugas`,
        position: 'top',
        timeout: 3000,
      })

      // Kembali ke halaman jadwal
      kembaliKeJadwal()

      // Refresh riwayat
      await loadRiwayatGaji()
    }
  } catch (error) {
    console.error('❌ Error saving gaji:', error)
    $q.notify({
      type: 'negative',
      message: error.response?.data?.message || 'Gagal menyimpan gaji',
      caption: error.message,
      timeout: 3000,
    })
  } finally {
    saving.value = false
  }
}

const loadRiwayatGaji = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${API_URL}/api/gaji/riwayat`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (res.data.success) {
      riwayatGaji.value = res.data.data
      console.log('📜 Riwayat gaji loaded:', riwayatGaji.value.length, 'items')
    }
  } catch (error) {
    console.error('❌ Error loading riwayat gaji:', error)
  }
}

// Lifecycle
onMounted(() => {
  console.log('🚀 GajiAdmin mounted')
  loadJadwal()
  loadRiwayatGaji()
})
</script>

<style scoped>
.hover-shadow-2:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.hover-shadow-3:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.rounded-borders {
  border-radius: 8px;
}

.table-responsive {
  overflow-x: auto;
}

.q-table th {
  font-weight: bold;
  background-color: #f5f5f5;
}

.q-table td,
.q-table th {
  padding: 12px 8px;
  white-space: nowrap;
}
</style>
