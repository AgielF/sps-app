<template>
  <q-page class="q-pa-md bg-green-1">
    <!-- Header -->
    <div class="row items-center q-mb-md">
      <div class="col">
        <div class="text-h6 text-weight-bold text-dark">Keuangan</div>
        <div class="text-caption text-grey-7">
          Kelola pemasukan dan pengeluaran |
          <span class="text-primary">{{ petugasName }}</span>
        </div>
      </div>
      <div class="col-auto">
        <div class="row q-gutter-sm">
          <q-btn
            label="Tambah Pemasukan"
            color="positive"
            icon="add"
            @click="showAddPemasukan"
            class="q-px-sm"
          />
          <q-btn
            label="Tambah Pengeluaran"
            color="negative"
            icon="remove"
            @click="showAddPengeluaran"
            class="q-px-sm"
          />
          <q-btn icon="refresh" color="grey" flat round @click="loadData" />
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center q-py-lg">
      <q-spinner color="primary" size="2em" />
      <div class="text-grey-7 q-mt-sm">Memuat data keuangan...</div>
    </div>

    <!-- Main Content -->
    <div v-else>
      <!-- Stats Cards -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-6 col-md-3">
          <q-card class="stat-card text-center bg-blue-1">
            <q-card-section>
              <div class="text-h6 text-blue">{{ formatCurrency(totalPemasukan) }}</div>
              <div class="text-caption text-grey-7">Total Pemasukan</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6 col-md-3">
          <q-card class="stat-card text-center bg-red-1">
            <q-card-section>
              <div class="text-h6 text-red">{{ formatCurrency(totalPengeluaran) }}</div>
              <div class="text-caption text-grey-7">Total Pengeluaran</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6 col-md-3">
          <q-card class="stat-card text-center bg-green-1">
            <q-card-section>
              <div class="text-h6 text-green">{{ formatCurrency(saldo) }}</div>
              <div class="text-caption text-grey-7">Saldo</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6 col-md-3">
          <q-card class="stat-card text-center bg-orange-1">
            <q-card-section>
              <div class="text-h6 text-orange">{{ formatCurrency(rataPengeluaran) }}</div>
              <div class="text-caption text-grey-7">Rata-rata/Bulan</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Filter Section -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-12 col-md-3">
          <q-select
            v-model="filter.bulan"
            label="Filter Bulan"
            outlined
            dense
            :options="bulanOptions"
            clearable
            emit-value
            map-options
          />
        </div>
        <div class="col-12 col-md-3">
          <q-input
            v-model="filter.tahun"
            label="Tahun"
            outlined
            dense
            type="number"
            :min="2020"
            :max="new Date().getFullYear()"
            clearable
          />
        </div>
        <div class="col-12 col-md-3">
          <q-select
            v-model="filter.tipe"
            label="Filter Tipe"
            outlined
            dense
            :options="tipeOptions"
            clearable
            emit-value
            map-options
          />
        </div>
        <div class="col-12 col-md-3">
          <q-input v-model="filter.search" label="Cari Keterangan" outlined dense clearable>
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </div>

      <!-- Tabs untuk Pemasukan & Pengeluaran -->
      <q-tabs
        v-model="activeTab"
        dense
        class="text-grey-7 q-mb-md"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
      >
        <q-tab name="pemasukan" icon="trending_up" label="Pemasukan" />
        <q-tab name="pengeluaran" icon="trending_down" label="Pengeluaran" />
        <q-tab name="semua" icon="list" label="Semua Transaksi" />
      </q-tabs>

      <q-tab-panels v-model="activeTab" animated>
        <!-- Pemasukan Panel -->
        <q-tab-panel name="pemasukan">
          <q-card class="data-card">
            <q-table
              :rows="filteredPemasukan"
              :columns="columnsPemasukan"
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
                      {{ formatDateSimple(props.row.tanggal) }}
                    </div>
                    <div class="text-caption text-grey-7">
                      {{ getDayName(props.row.tanggal) }}
                    </div>
                  </div>
                </q-td>
              </template>

              <!-- Jumlah Column -->
              <template v-slot:body-cell-jumlah="props">
                <q-td :props="props">
                  <div class="text-weight-bold text-green">
                    {{ formatCurrency(props.row.jumlah) }}
                  </div>
                </q-td>
              </template>

              <!-- Kategori Column -->
              <template v-slot:body-cell-kategori="props">
                <q-td :props="props">
                  <q-badge :color="getCategoryColor(props.row.kategori)">
                    {{ props.row.kategori || '-' }}
                  </q-badge>
                </q-td>
              </template>

              <!-- Petugas Column -->
              <template v-slot:body-cell-petugas="props">
                <q-td :props="props">
                  <div class="text-caption text-grey-7">
                    {{ props.row.petugas || 'Admin' }}
                  </div>
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
                      @click="editPemasukan(props.row)"
                    />
                    <q-btn
                      icon="delete"
                      size="sm"
                      color="red"
                      flat
                      dense
                      @click="deletePemasukan(props.row.id, props.row.keterangan)"
                    />
                  </div>
                </q-td>
              </template>

              <!-- Empty State -->
              <template v-slot:no-data>
                <div class="full-width row flex-center text-grey q-pa-xl">
                  <q-icon name="payments" size="3em" color="grey-4" class="q-mb-sm" />
                  <div class="text-center">
                    <div class="text-subtitle1 text-grey-7 q-mb-xs">Belum ada data pemasukan</div>
                    <div class="text-caption text-grey-6">
                      Mulai dengan menambahkan pemasukan baru
                    </div>
                    <q-btn
                      label="Tambah Pemasukan"
                      color="positive"
                      outline
                      class="q-mt-md"
                      @click="showAddPemasukan"
                    />
                  </div>
                </div>
              </template>
            </q-table>
          </q-card>
        </q-tab-panel>

        <!-- Pengeluaran Panel -->
        <q-tab-panel name="pengeluaran">
          <q-card class="data-card">
            <q-table
              :rows="filteredPengeluaran"
              :columns="columnsPengeluaran"
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
                      {{ formatDateSimple(props.row.tanggal) }}
                    </div>
                    <div class="text-caption text-grey-7">
                      {{ getDayName(props.row.tanggal) }}
                    </div>
                  </div>
                </q-td>
              </template>

              <!-- Jumlah Column -->
              <template v-slot:body-cell-jumlah="props">
                <q-td :props="props">
                  <div class="text-weight-bold text-red">
                    {{ formatCurrency(props.row.jumlah) }}
                  </div>
                </q-td>
              </template>

              <!-- Kategori Column -->
              <template v-slot:body-cell-kategori="props">
                <q-td :props="props">
                  <q-badge :color="getCategoryColor(props.row.kategori)">
                    {{ props.row.kategori || '-' }}
                  </q-badge>
                </q-td>
              </template>

              <!-- Petugas Column -->
              <template v-slot:body-cell-petugas="props">
                <q-td :props="props">
                  <div class="text-caption text-grey-7">
                    {{ props.row.petugas || 'Admin' }}
                  </div>
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
                      @click="editPengeluaran(props.row)"
                    />
                    <q-btn
                      icon="delete"
                      size="sm"
                      color="red"
                      flat
                      dense
                      @click="deletePengeluaran(props.row.id, props.row.keterangan)"
                    />
                  </div>
                </q-td>
              </template>

              <!-- Empty State -->
              <template v-slot:no-data>
                <div class="full-width row flex-center text-grey q-pa-xl">
                  <q-icon name="money_off" size="3em" color="grey-4" class="q-mb-sm" />
                  <div class="text-center">
                    <div class="text-subtitle1 text-grey-7 q-mb-xs">Belum ada data pengeluaran</div>
                    <div class="text-caption text-grey-6">
                      Mulai dengan menambahkan pengeluaran baru
                    </div>
                    <q-btn
                      label="Tambah Pengeluaran"
                      color="negative"
                      outline
                      class="q-mt-md"
                      @click="showAddPengeluaran"
                    />
                  </div>
                </div>
              </template>
            </q-table>
          </q-card>
        </q-tab-panel>

        <!-- Semua Transaksi Panel -->
        <q-tab-panel name="semua">
          <q-card class="data-card">
            <q-table
              :rows="allTransactions"
              :columns="columnsAll"
              row-key="id"
              flat
              bordered
              :pagination="{ rowsPerPage: 15 }"
              :loading="loading"
            >
              <!-- Tanggal Column -->
              <template v-slot:body-cell-tanggal="props">
                <q-td :props="props">
                  <div class="column">
                    <div class="text-weight-medium">
                      {{ formatDateSimple(props.row.tanggal) }}
                    </div>
                    <div class="text-caption text-grey-7">
                      {{ getDayName(props.row.tanggal) }}
                    </div>
                  </div>
                </q-td>
              </template>

              <!-- Tipe Column -->
              <template v-slot:body-cell-tipe="props">
                <q-td :props="props">
                  <q-badge :color="props.row.tipe === 'pemasukan' ? 'green' : 'red'">
                    {{ props.row.tipe === 'pemasukan' ? 'Pemasukan' : 'Pengeluaran' }}
                  </q-badge>
                </q-td>
              </template>

              <!-- Jumlah Column -->
              <template v-slot:body-cell-jumlah="props">
                <q-td :props="props">
                  <div
                    :class="
                      props.row.tipe === 'pemasukan'
                        ? 'text-weight-bold text-green'
                        : 'text-weight-bold text-red'
                    "
                  >
                    {{ props.row.tipe === 'pemasukan' ? '+' : '-' }}
                    {{ formatCurrency(props.row.jumlah) }}
                  </div>
                </q-td>
              </template>

              <!-- Petugas Column -->
              <template v-slot:body-cell-petugas="props">
                <q-td :props="props">
                  <div class="text-caption text-grey-7">
                    {{ props.row.petugas || 'Admin' }}
                  </div>
                </q-td>
              </template>

              <!-- Empty State -->
              <template v-slot:no-data>
                <div class="full-width row flex-center text-grey q-pa-xl">
                  <q-icon name="account_balance_wallet" size="3em" color="grey-4" class="q-mb-sm" />
                  <div class="text-center">
                    <div class="text-subtitle1 text-grey-7 q-mb-xs">Belum ada transaksi</div>
                    <div class="text-caption text-grey-6">
                      Mulai dengan menambahkan transaksi baru
                    </div>
                  </div>
                </div>
              </template>
            </q-table>
          </q-card>
        </q-tab-panel>
      </q-tab-panels>

      <!-- Chart Section -->
      <div class="row q-col-gutter-md q-mt-lg">
        <div class="col-12 col-md-6">
          <q-card class="chart-card">
            <q-card-section>
              <div class="text-subtitle1 text-weight-bold">Pemasukan vs Pengeluaran</div>
              <div class="text-caption text-grey-7">Perbandingan bulan ini</div>
            </q-card-section>
            <q-card-section>
              <div class="chart-placeholder">
                <div class="text-center q-py-xl">
                  <q-icon name="bar_chart" size="3em" color="grey-4" />
                  <div class="text-caption text-grey-6 q-mt-sm">Chart akan ditampilkan di sini</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-6">
          <q-card class="chart-card">
            <q-card-section>
              <div class="text-subtitle1 text-weight-bold">Kategori Pengeluaran</div>
              <div class="text-caption text-grey-7">Distribusi pengeluaran bulan ini</div>
            </q-card-section>
            <q-card-section>
              <div class="chart-placeholder">
                <div class="text-center q-py-xl">
                  <q-icon name="pie_chart" size="3em" color="grey-4" />
                  <div class="text-caption text-grey-6 q-mt-sm">Chart akan ditampilkan di sini</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Dialog Form Pemasukan -->
    <q-dialog v-model="showPemasukanDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ isEditPemasukan ? 'Edit Pemasukan' : 'Tambah Pemasukan' }}</div>
          <div class="text-caption text-grey-7">Petugas: {{ petugasName }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="savePemasukan" class="q-gutter-md">
            <q-input
              v-model="pemasukanForm.tanggal"
              label="Tanggal"
              outlined
              type="date"
              :rules="[(val) => !!val || 'Tanggal wajib diisi']"
            />

            <q-input
              v-model="pemasukanForm.jumlah"
              label="Jumlah"
              outlined
              type="number"
              prefix="Rp"
              :rules="[(val) => val > 0 || 'Jumlah harus lebih dari 0']"
            />

            <q-select
              v-model="pemasukanForm.kategori"
              label="Kategori"
              outlined
              :options="kategoriPemasukan"
              :rules="[(val) => !!val || 'Kategori wajib dipilih']"
            />

            <q-input
              v-model="pemasukanForm.keterangan"
              label="Keterangan"
              outlined
              type="textarea"
              rows="2"
              :rules="[(val) => !!val || 'Keterangan wajib diisi']"
            />

            <div class="row q-gutter-sm">
              <q-checkbox
                v-model="pemasukanForm.status_bayar"
                label="Status Lunas"
                true-value="lunas"
                false-value="belum"
              />
              <q-select
                v-model="pemasukanForm.metode_bayar"
                label="Metode Bayar"
                outlined
                dense
                :options="metodeBayarOptions"
              />
            </div>

            <div class="row justify-end q-gutter-sm q-mt-md">
              <q-btn label="Batal" color="grey" flat v-close-popup />
              <q-btn
                :label="isEditPemasukan ? 'Update' : 'Simpan'"
                color="positive"
                type="submit"
                :loading="saving"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog Form Pengeluaran -->
    <q-dialog v-model="showPengeluaranDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">
            {{ isEditPengeluaran ? 'Edit Pengeluaran' : 'Tambah Pengeluaran' }}
          </div>
          <div class="text-caption text-grey-7">Petugas: {{ petugasName }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="savePengeluaran" class="q-gutter-md">
            <q-input
              v-model="pengeluaranForm.tanggal"
              label="Tanggal"
              outlined
              type="date"
              :rules="[(val) => !!val || 'Tanggal wajib diisi']"
            />

            <q-input
              v-model="pengeluaranForm.jumlah"
              label="Jumlah"
              outlined
              type="number"
              prefix="Rp"
              :rules="[(val) => val > 0 || 'Jumlah harus lebih dari 0']"
            />

            <q-select
              v-model="pengeluaranForm.kategori"
              label="Kategori"
              outlined
              :options="kategoriPengeluaran"
              :rules="[(val) => !!val || 'Kategori wajib dipilih']"
            />

            <q-input
              v-model="pengeluaranForm.keterangan"
              label="Keterangan"
              outlined
              type="textarea"
              rows="2"
              :rules="[(val) => !!val || 'Keterangan wajib diisi']"
            />

            <div class="row q-gutter-sm">
              <q-checkbox
                v-model="pengeluaranForm.status_bayar"
                label="Status Lunas"
                true-value="lunas"
                false-value="belum"
              />
              <q-select
                v-model="pengeluaranForm.metode_bayar"
                label="Metode Bayar"
                outlined
                dense
                :options="metodeBayarOptions"
              />
            </div>

            <div class="row justify-end q-gutter-sm q-mt-md">
              <q-btn label="Batal" color="grey" flat v-close-popup />
              <q-btn
                :label="isEditPengeluaran ? 'Update' : 'Simpan'"
                color="negative"
                type="submit"
                :loading="saving"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar, date } from 'quasar'
import axios from 'axios'

const $q = useQuasar()

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

// States
const loading = ref(true)
const saving = ref(false)
const activeTab = ref('pemasukan')
const showPemasukanDialog = ref(false)
const showPengeluaranDialog = ref(false)
const isEditPemasukan = ref(false)
const isEditPengeluaran = ref(false)
const petugasName = ref('')

// Data
const pemasukanList = ref([])
const pengeluaranList = ref([])

// Filter
const filter = ref({
  bulan: '',
  tahun: new Date().getFullYear(),
  tipe: '',
  search: '',
})

// Forms
const pemasukanForm = ref({
  id: null,
  tanggal: new Date().toISOString().split('T')[0],
  jumlah: '',
  kategori: '',
  keterangan: '',
  petugas: '',
  status_bayar: 'lunas',
  metode_bayar: 'cash',
})

const pengeluaranForm = ref({
  id: null,
  tanggal: new Date().toISOString().split('T')[0],
  jumlah: '',
  kategori: '',
  keterangan: '',
  petugas: '',
  status_bayar: 'lunas',
  metodo_bayar: 'cash',
})

// Options
const bulanOptions = [
  { label: 'Januari', value: 1 },
  { label: 'Februari', value: 2 },
  { label: 'Maret', value: 3 },
  { label: 'April', value: 4 },
  { label: 'Mei', value: 5 },
  { label: 'Juni', value: 6 },
  { label: 'Juli', value: 7 },
  { label: 'Agustus', value: 8 },
  { label: 'September', value: 9 },
  { label: 'Oktober', value: 10 },
  { label: 'November', value: 11 },
  { label: 'Desember', value: 12 },
]

const tipeOptions = [
  { label: 'Pemasukan', value: 'pemasukan' },
  { label: 'Pengeluaran', value: 'pengeluaran' },
]

const kategoriPemasukan = ['Iuran Warga', 'Denda', 'Bantuan', 'Lain-lain']

const kategoriPengeluaran = [
  'Gaji Petugas',
  'Operasional',
  'Perawatan Alat',
  'Transportasi',
  'Listrik/Air',
  'Lain-lain',
]

const metodeBayarOptions = ['cash', 'transfer', 'qris']

// Columns
const columnsPemasukan = [
  { name: 'tanggal', label: 'Tanggal', field: 'tanggal', align: 'left', sortable: true },
  { name: 'kategori', label: 'Kategori', field: 'kategori', align: 'left', sortable: true },
  { name: 'keterangan', label: 'Keterangan', field: 'keterangan', align: 'left', sortable: true },
  { name: 'jumlah', label: 'Jumlah', field: 'jumlah', align: 'right', sortable: true },
  { name: 'petugas', label: 'Input By', field: 'petugas', align: 'left' },
  { name: 'actions', label: 'Aksi', align: 'center' },
]

const columnsPengeluaran = [
  { name: 'tanggal', label: 'Tanggal', field: 'tanggal', align: 'left', sortable: true },
  { name: 'kategori', label: 'Kategori', field: 'kategori', align: 'left', sortable: true },
  { name: 'keterangan', label: 'Keterangan', field: 'keterangan', align: 'left', sortable: true },
  { name: 'jumlah', label: 'Jumlah', field: 'jumlah', align: 'right', sortable: true },
  { name: 'petugas', label: 'Input By', field: 'petugas', align: 'left' },
  { name: 'actions', label: 'Aksi', align: 'center' },
]

const columnsAll = [
  { name: 'tanggal', label: 'Tanggal', field: 'tanggal', align: 'left', sortable: true },
  { name: 'tipe', label: 'Tipe', field: 'tipe', align: 'center', sortable: true },
  { name: 'kategori', label: 'Kategori', field: 'kategori', align: 'left', sortable: true },
  { name: 'keterangan', label: 'Keterangan', field: 'keterangan', align: 'left', sortable: true },
  { name: 'jumlah', label: 'Jumlah', field: 'jumlah', align: 'right', sortable: true },
  { name: 'petugas', label: 'Input By', field: 'petugas', align: 'left' },
]

// Computed Properties
const filteredPemasukan = computed(() => {
  let filtered = pemasukanList.value

  if (filter.value.bulan) {
    filtered = filtered.filter((item) => {
      const dateObj = new Date(item.tanggal)
      return dateObj.getMonth() + 1 === parseInt(filter.value.bulan)
    })
  }

  if (filter.value.tahun) {
    filtered = filtered.filter((item) => {
      const dateObj = new Date(item.tanggal)
      return dateObj.getFullYear() === parseInt(filter.value.tahun)
    })
  }

  if (filter.value.search) {
    const search = filter.value.search.toLowerCase()
    filtered = filtered.filter(
      (item) =>
        item.keterangan?.toLowerCase().includes(search) ||
        item.kategori?.toLowerCase().includes(search),
    )
  }

  return filtered.sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal))
})

const filteredPengeluaran = computed(() => {
  let filtered = pengeluaranList.value

  if (filter.value.bulan) {
    filtered = filtered.filter((item) => {
      const dateObj = new Date(item.tanggal)
      return dateObj.getMonth() + 1 === parseInt(filter.value.bulan)
    })
  }

  if (filter.value.tahun) {
    filtered = filtered.filter((item) => {
      const dateObj = new Date(item.tanggal)
      return dateObj.getFullYear() === parseInt(filter.value.tahun)
    })
  }

  if (filter.value.search) {
    const search = filter.value.search.toLowerCase()
    filtered = filtered.filter(
      (item) =>
        item.keterangan?.toLowerCase().includes(search) ||
        item.kategori?.toLowerCase().includes(search),
    )
  }

  return filtered.sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal))
})

const allTransactions = computed(() => {
  const pemasukan = filteredPemasukan.value.map((item) => ({
    ...item,
    tipe: 'pemasukan',
  }))

  const pengeluaran = filteredPengeluaran.value.map((item) => ({
    ...item,
    tipe: item.kategori === 'Gaji Petugas' ? 'gaji' : 'pengeluaran',
  }))

  return [...pemasukan, ...pengeluaran].sort((a, b) => new Date(b.tanggal) - new Date(a.tanggal))
})

const totalPemasukan = computed(() => {
  return filteredPemasukan.value.reduce((sum, item) => sum + (parseFloat(item.jumlah) || 0), 0)
})

const totalPengeluaran = computed(() => {
  return filteredPengeluaran.value.reduce((sum, item) => sum + (parseFloat(item.jumlah) || 0), 0)
})

const saldo = computed(() => totalPemasukan.value - totalPengeluaran.value)

const rataPengeluaran = computed(() => {
  const count = filteredPengeluaran.value.length
  return count > 0 ? totalPengeluaran.value / count : 0
})

// Helper Functions

const formatDateSimple = (dateString) => {
  if (!dateString) return '-'

  try {
    return date.formatDate(dateString, 'DD/MM')
  } catch {
    if (typeof dateString === 'string' && dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      const [month, day] = dateString.split('-')
      return `${day}/${month}`
    }

    const d = new Date(dateString)
    if (!isNaN(d.getTime())) {
      const day = String(d.getDate()).padStart(2, '0')
      const month = String(d.getMonth() + 1).padStart(2, '0')
      return `${day}/${month}`
    }

    return dateString || '-'
  }
}

const getDayName = (dateString) => {
  if (!dateString) return ''

  try {
    return date.formatDate(dateString, 'dddd')
  } catch {
    try {
      const days = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
      const d = new Date(dateString)
      return days[d.getDay()]
    } catch {
      return ''
    }
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
  }).format(amount)
}

const getCategoryColor = (category) => {
  const colors = {
    'Iuran Warga': 'blue',
    Denda: 'orange',
    Bantuan: 'green',
    'Gaji Petugas': 'purple',
    Operasional: 'teal',
    'Perawatan Alat': 'cyan',
    Transportasi: 'amber',
    'Listrik/Air': 'light-blue',
    'Lain-lain': 'grey',
  }
  return colors[category] || 'grey'
}

// Methods
const loadData = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    petugasName.value = user.username || user.name || 'Admin'

    // Load pemasukan
    const pemasukanRes = await axios.get(`${API_URL}/api/keuangan/pemasukan`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    console.log('✅ Pemasukan data:', pemasukanRes.data.data)

    if (pemasukanRes.data.success) {
      pemasukanList.value = pemasukanRes.data.data
    }

    // Load pengeluaran
    const pengeluaranRes = await axios.get(`${API_URL}/api/keuangan/pengeluaran`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    console.log('✅ Pengeluaran data:', pengeluaranRes.data.data)

    if (pengeluaranRes.data.success) {
      pengeluaranList.value = pengeluaranRes.data.data
    }
  } catch (error) {
    console.error('Error loading data:', error)
    $q.notify({
      type: 'negative',
      message: 'Gagal memuat data keuangan',
      position: 'top',
    })
  } finally {
    loading.value = false
  }
}

const showAddPemasukan = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  pemasukanForm.value = {
    id: null,
    tanggal: new Date().toISOString().split('T')[0],
    jumlah: '',
    kategori: '',
    keterangan: '',
    petugas: user.username || user.name || 'Admin',
    status_bayar: 'lunas',
    metode_bayar: 'cash',
  }
  isEditPemasukan.value = false
  showPemasukanDialog.value = true
}

const showAddPengeluaran = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  pengeluaranForm.value = {
    id: null,
    tanggal: new Date().toISOString().split('T')[0],
    jumlah: '',
    kategori: '',
    keterangan: '',
    petugas: user.username || user.name || 'Admin',
    status_bayar: 'lunas',
    metode_bayar: 'cash',
  }
  isEditPengeluaran.value = false
  showPengeluaranDialog.value = true
}

const editPemasukan = (item) => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  pemasukanForm.value = {
    ...item,
    petugas: user.username || user.name || 'Admin',
  }
  isEditPemasukan.value = true
  showPemasukanDialog.value = true
}

const editPengeluaran = (item) => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  pengeluaranForm.value = {
    ...item,
    petugas: user.username || user.name || 'Admin',
  }
  isEditPengeluaran.value = true
  showPengeluaranDialog.value = true
}

const savePemasukan = async () => {
  saving.value = true
  try {
    const token = localStorage.getItem('token')
    const user = JSON.parse(localStorage.getItem('user') || '{}')

    const dataToSend = {
      ...pemasukanForm.value,
      petugas: user.username || user.name || 'Admin',
    }

    const method = isEditPemasukan.value ? 'PUT' : 'POST'
    const url = isEditPemasukan.value
      ? `${API_URL}/api/keuangan/pemasukan/${dataToSend.id}`
      : `${API_URL}/api/keuangan/pemasukan`

    console.log('📤 Sending pemasukan data:', dataToSend)

    const response = await axios({
      method,
      url,
      data: dataToSend,
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (response.data.success) {
      $q.notify({
        type: 'positive',
        message: isEditPemasukan.value
          ? 'Pemasukan berhasil diperbarui'
          : 'Pemasukan berhasil ditambahkan',
        position: 'top',
      })

      showPemasukanDialog.value = false
      await loadData()
    }
  } catch (error) {
    console.error('Error saving pemasukan:', error)
    $q.notify({
      type: 'negative',
      message: error.response?.data?.message || 'Gagal menyimpan pemasukan',
      position: 'top',
    })
  } finally {
    saving.value = false
  }
}

const savePengeluaran = async () => {
  saving.value = true
  try {
    const token = localStorage.getItem('token')
    const user = JSON.parse(localStorage.getItem('user') || '{}')

    const dataToSend = {
      ...pengeluaranForm.value,
      petugas: user.username || user.name || 'Admin',
    }

    const method = isEditPengeluaran.value ? 'PUT' : 'POST'
    const url = isEditPengeluaran.value
      ? `${API_URL}/api/keuangan/pengeluaran/${dataToSend.id}`
      : `${API_URL}/api/keuangan/pengeluaran`

    console.log('📤 Sending pengeluaran data:', dataToSend)

    const response = await axios({
      method,
      url,
      data: dataToSend,
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (response.data.success) {
      $q.notify({
        type: 'positive',
        message: isEditPengeluaran.value
          ? 'Pengeluaran berhasil diperbarui'
          : 'Pengeluaran berhasil ditambahkan',
        position: 'top',
      })

      showPengeluaranDialog.value = false
      await loadData()
    }
  } catch (error) {
    console.error('Error saving pengeluaran:', error)
    $q.notify({
      type: 'negative',
      message: error.response?.data?.message || 'Gagal menyimpan pengeluaran',
      position: 'top',
    })
  } finally {
    saving.value = false
  }
}

const deletePemasukan = async (id, keterangan) => {
  $q.dialog({
    title: 'Konfirmasi Hapus',
    message: `Yakin ingin menghapus pemasukan <strong>${keterangan || 'ini'}</strong>?`,
    html: true,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.delete(`${API_URL}/api/keuangan/pemasukan/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (response.data.success) {
        $q.notify({
          type: 'positive',
          message: 'Pemasukan berhasil dihapus',
          position: 'top',
        })
        await loadData()
      }
    } catch (error) {
      console.error('Error deleting pemasukan:', error)
      $q.notify({
        type: 'negative',
        message: error.response?.data?.message || 'Gagal menghapus pemasukan',
        position: 'top',
      })
    }
  })
}

const deletePengeluaran = async (id, keterangan) => {
  $q.dialog({
    title: 'Konfirmasi Hapus',
    message: `Yakin ingin menghapus pengeluaran <strong>${keterangan || 'ini'}</strong>?`,
    html: true,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.delete(`${API_URL}/api/keuangan/pengeluaran/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (response.data.success) {
        $q.notify({
          type: 'positive',
          message: 'Pengeluaran berhasil dihapus',
          position: 'top',
        })
        await loadData()
      }
    } catch (error) {
      console.error('Error deleting pengeluaran:', error)
      $q.notify({
        type: 'negative',
        message: error.response?.data?.message || 'Gagal menghapus pengeluaran',
        position: 'top',
      })
    }
  })
}

// Lifecycle
onMounted(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  petugasName.value = user.username || user.name || 'Admin'

  loadData()
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

.chart-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
}
</style>
