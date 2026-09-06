<template>
  <q-page class="bg-grey-1">
    <!-- Header dengan background gradient -->
    <div class="header-gradient q-pa-md q-pb-lg">
      <div class="row items-center q-mb-md"></div>

      <div class="q-mb-lg">
        <div class="text-h4 text-weight-bold text-white">Riwayat & Laporan</div>
        <div class="text-subtitle1 text-white text-opacity-80">
          Monitor semua aktivitas sampah Anda
        </div>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="q-px-md" style="margin-top: -20px">
      <q-card class="filter-card shadow-3">
        <q-card-section>
          <div class="row items-center q-col-gutter-md">
            <!-- Bulan -->
            <div class="col-md-3 col-12">
              <q-select
                v-model="bulanDipilih"
                :options="opsiBulan"
                label="Pilih Bulan"
                filled
                dense
                emit-value
                map-options
                clearable
                @update:model-value="handleBulanChange"
                :loading="loadingBulan"
              >
                <template v-slot:prepend>
                  <q-icon name="calendar_month" color="primary" />
                </template>
                <template v-slot:option="scope">
                  <q-item v-bind="scope.itemProps">
                    <q-item-section>
                      <q-item-label class="text-weight-medium">
                        {{ scope.opt.label }}
                      </q-item-label>
                      <q-item-label caption class="text-primary">
                        {{ scope.opt.count }} data
                      </q-item-label>
                    </q-item-section>
                    <q-item-section side v-if="scope.opt.isCurrent">
                      <q-badge color="primary" label="Bulan ini" />
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
            </div>

            <!-- Tipe Data -->
            <div class="col-md-3 col-12">
              <q-select
                v-model="tipeFilter"
                :options="tipeOptions"
                label="Jenis Data"
                filled
                dense
                emit-value
                map-options
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="category" color="primary" />
                </template>
              </q-select>
            </div>

            <!-- Status Filter -->
            <div class="col-md-3 col-12">
              <q-select
                v-model="statusFilter"
                :options="statusOptions"
                label="Filter Status"
                filled
                dense
                multiple
                clearable
                use-chips
                emit-value
                map-options
              >
                <template v-slot:prepend>
                  <q-icon name="filter_alt" color="primary" />
                </template>
                <template v-slot:selected-item="scope">
                  <q-chip
                    dense
                    removable
                    @remove="scope.removeAtIndex(scope.index)"
                    :color="getStatusColor(scope.opt.value)"
                    text-color="white"
                  >
                    {{ scope.opt.label }}
                  </q-chip>
                </template>
              </q-select>
            </div>

            <!-- Search -->
            <div class="col-md-3 col-12">
              <q-input v-model="searchQuery" placeholder="Cari riwayat..." filled dense clearable>
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
          </div>

          <!-- Advanced Filters Toggle -->
          <div class="q-mt-md">
            <q-btn
              flat
              dense
              :icon="showAdvancedFilters ? 'expand_less' : 'expand_more'"
              label="Filter Lanjutan"
              @click="showAdvancedFilters = !showAdvancedFilters"
              class="text-primary"
              size="sm"
            />
          </div>

          <!-- Advanced Filters -->
          <q-slide-transition>
            <div v-show="showAdvancedFilters" class="q-mt-md">
              <div class="row items-center q-col-gutter-md">
                <div class="col-md-3 col-12">
                  <q-input
                    v-model="minKarung"
                    type="number"
                    label="Min Karung"
                    filled
                    dense
                    clearable
                    min="0"
                  >
                    <template v-slot:prepend>
                      <q-icon name="numbers" />
                    </template>
                  </q-input>
                </div>
                <div class="col-md-3 col-12">
                  <q-input
                    v-model="maxKarung"
                    type="number"
                    label="Max Karung"
                    filled
                    dense
                    clearable
                    min="0"
                  >
                    <template v-slot:prepend>
                      <q-icon name="numbers" />
                    </template>
                  </q-input>
                </div>
                <div class="col-md-3 col-12">
                  <q-input
                    v-model="startDate"
                    label="Dari Tanggal"
                    filled
                    dense
                    type="date"
                    clearable
                  />
                </div>
                <div class="col-md-3 col-12">
                  <q-input
                    v-model="endDate"
                    label="Sampai Tanggal"
                    filled
                    dense
                    type="date"
                    clearable
                    :min="startDate"
                  />
                </div>
              </div>
              <div class="row justify-end q-mt-sm">
                <q-btn
                  flat
                  label="Reset Filter"
                  @click="resetFilters"
                  class="text-grey-7"
                  size="sm"
                />
                <q-btn
                  label="Terapkan"
                  color="primary"
                  @click="applyAdvancedFilters"
                  class="q-ml-sm"
                  size="sm"
                />
              </div>
            </div>
          </q-slide-transition>
        </q-card-section>
      </q-card>
    </div>

    <!-- Content -->
    <div class="q-pa-md">
      <!-- Header Content -->
      <div class="row items-center justify-between q-mb-lg">
        <div class="col">
          <div class="text-h6 text-weight-bold text-dark">
            {{ tampilJudulBulan }}
            <q-badge v-if="filteredRiwayat.length > 0" color="primary" class="q-ml-sm">
              {{ filteredRiwayat.length }} dari {{ semuaRiwayat.length }} data
            </q-badge>
          </div>
          <div class="text-caption text-grey-7 q-mt-xs">
            <span v-if="tipeFilter !== 'transaksi'"
              >Total karung: <strong>{{ totalKarung }}</strong> karung •
            </span>
            <span v-if="tipeFilter === 'transaksi'"
              >Total transaksi: <strong>{{ stats.transaksi.total }}</strong> •
            </span>
            Saldo: <strong>Rp {{ formatCurrency(saldo) }}</strong>
          </div>
        </div>
        <div class="col-auto">
          <div class="row items-center q-gutter-sm">
            <q-btn
              round
              flat
              icon="refresh"
              color="primary"
              @click="loadRiwayat"
              :loading="loading"
            />
            <q-btn
              round
              flat
              icon="grid_view"
              color="primary"
              @click="viewMode = 'grid'"
              :class="{ 'bg-primary text-white': viewMode === 'grid' }"
            />
            <q-btn
              round
              flat
              icon="view_list"
              color="primary"
              @click="viewMode = 'list'"
              :class="{ 'bg-primary text-white': viewMode === 'list' }"
            />
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner-grid color="primary" size="3em" />
        <div class="text-grey-7 q-mt-md">Memuat riwayat...</div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center q-py-xl">
        <q-icon name="error_outline" size="80px" color="negative" />
        <div class="text-h6 text-negative q-mt-md">Gagal memuat data</div>
        <div class="text-caption text-grey-7 q-mt-sm q-mb-md">
          {{ errorMessage }}
        </div>
        <q-btn color="primary" label="Coba Lagi" @click="loadRiwayat" />
      </div>

      <!-- Data Empty -->
      <div v-else-if="semuaRiwayat.length === 0" class="text-center q-py-xl">
        <div class="illustration-container q-mb-md">
          <q-icon name="inventory_2" size="120px" color="grey-4" />
          <div class="floating-icon">
            <q-icon name="recycling" size="40px" color="primary" />
          </div>
        </div>
        <div class="text-h5 text-grey-6 q-mt-md">Belum ada riwayat</div>
        <div class="text-caption text-grey-6 q-mt-sm q-mb-lg">
          Anda belum memiliki riwayat laporan atau transaksi
        </div>
        <q-btn color="primary" label="Buat Laporan" @click="createLaporan" />
      </div>

      <!-- Data Content -->
      <div v-else>
        <!-- Empty Filter Result -->
        <div v-if="filteredRiwayat.length === 0" class="text-center q-py-xl">
          <q-icon name="search_off" size="80px" color="grey-4" />
          <div class="text-h6 text-grey-5 q-mt-md">Tidak ditemukan</div>
          <div class="text-caption text-grey-6 q-mt-sm">
            Tidak ada data yang sesuai dengan filter Anda
          </div>
          <q-btn flat label="Reset Filter" @click="resetFilters" color="primary" class="q-mt-sm" />
        </div>

        <!-- Grid View -->
        <div v-else-if="viewMode === 'grid' && $q.screen.gt.xs" class="row q-col-gutter-md">
          <div
            v-for="item in paginatedRiwayat"
            :key="item.id + '-' + item.tipe"
            class="col-12 col-sm-6 col-md-4"
          >
            <q-card class="riwayat-grid-card" flat bordered :class="getCardClass(item)">
              <q-card-section class="q-pa-md">
                <!-- Type Badge -->
                <div class="row justify-between items-center q-mb-sm">
                  <q-badge :color="getTipeColor(item.tipe)" class="tipe-badge">
                    {{ item.tipe === 'laporan' ? 'Laporan' : 'Transaksi' }}
                  </q-badge>
                  <q-icon
                    :name="getTipeIcon(item.tipe)"
                    :color="getTipeColor(item.tipe)"
                    size="20px"
                  />
                </div>

                <!-- Kode -->
                <div class="text-caption text-grey-7 q-mb-xs">
                  <q-icon name="tag" size="12px" class="q-mr-xs" />
                  {{ item.kode }}
                </div>

                <!-- Date & Time -->
                <div class="text-caption text-grey-7 q-mb-xs">
                  <q-icon name="calendar_today" size="12px" class="q-mr-xs" />
                  {{ item.tanggal_singkat }}
                </div>
                <div class="text-caption text-grey-7 q-mb-sm">
                  <q-icon name="schedule" size="12px" class="q-mr-xs" />
                  {{ item.waktu }}
                </div>

                <!-- Content -->
                <!-- Di Grid View -->
                <div class="text-center q-my-md">
                  <div class="text-h3 text-weight-bold" :class="getTextColor(item)">
                    {{
                      item.tipe === 'transaksi'
                        ? formatCurrency(item.jumlah)
                        : getDisplayJumlahKarung(item)
                    }}
                  </div>
                  <div class="text-caption text-grey-7">
                    {{ item.tipe === 'transaksi' ? formatJumlahKarung(item) : 'Estimasi Volume' }}
                  </div>
                  <div class="text-caption text-grey-7 q-mt-xs">
                    {{ item.jenis }}
                  </div>
                </div>

                <!-- Di List View -->
                <q-item-label class="text-weight-bold text-dark">
                  <span v-if="item.tipe === 'transaksi'">
                    {{ item.jenis }} - Rp {{ formatCurrency(item.jumlah) }}
                  </span>
                  <span v-else> {{ item.jenis }} - {{ getDisplayJumlahKarung(item) }} </span>
                </q-item-label>

                <!-- Status -->
                <div class="text-center q-mb-sm">
                  <q-badge :color="getStatusColor(item.status)" class="status-badge">
                    {{ formatStatus(item.status) }}
                  </q-badge>
                </div>

                <!-- Divider -->
                <q-separator class="q-my-sm" />

                <!-- Petugas Info -->
                <div class="text-caption" v-if="item.petugas?.nama">
                  <div class="row items-center q-mb-xs">
                    <q-icon name="person" size="14px" class="q-mr-xs" />
                    <span class="text-weight-medium">Petugas:</span>
                  </div>
                  <div class="text-grey-8 q-pl-lg">
                    {{ item.petugas.nama }}
                  </div>
                </div>

                <!-- Catatan -->
                <div v-if="item.catatan" class="text-caption q-mt-sm">
                  <div class="row items-center q-mb-xs">
                    <q-icon name="notes" size="14px" class="q-mr-xs" />
                    <span class="text-weight-medium">Catatan:</span>
                  </div>
                  <div class="text-grey-8 q-pl-lg">
                    {{ truncateText(item.catatan, 60) }}
                  </div>
                </div>

                <!-- Action Button -->
                <q-card-actions align="center" class="q-px-none q-pb-none q-pt-md">
                  <q-btn
                    flat
                    label="Detail"
                    color="primary"
                    size="sm"
                    @click="showDetail(item)"
                    class="full-width"
                  />
                </q-card-actions>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- List View -->
        <div v-else>
          <q-list bordered separator class="rounded-borders">
            <q-item
              v-for="item in paginatedRiwayat"
              :key="item.id + '-' + item.tipe"
              class="riwayat-list-item q-my-xs"
              clickable
              @click="showDetail(item)"
              :class="getListItemClass(item)"
            >
              <q-item-section avatar>
                <q-avatar
                  :color="getTipeColor(item.tipe)"
                  text-color="white"
                  size="50px"
                  class="shadow-1"
                >
                  <q-icon :name="getTipeIcon(item.tipe)" size="24px" />
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label class="text-weight-bold text-dark">
                  <span v-if="item.tipe === 'transaksi'">
                    {{ item.jenis }} - Rp {{ formatCurrency(item.jumlah) }}
                  </span>
                  <span v-else> {{ item.jenis }} - {{ item.jumlah_karung }} Karung </span>
                </q-item-label>
                <q-item-label caption lines="1">
                  <q-icon name="tag" size="12px" class="q-mr-xs" />
                  {{ item.kode }}
                </q-item-label>
                <q-item-label caption lines="1" class="q-mt-xs">
                  <q-icon name="person" size="12px" class="q-mr-xs" />
                  {{ item.petugas?.nama || 'Belum ada petugas' }}
                </q-item-label>
                <q-item-label caption lines="1" class="q-mt-xs">
                  <q-icon name="notes" size="12px" class="q-mr-xs" />
                  {{ item.catatan || 'Tidak ada catatan' }}
                </q-item-label>
              </q-item-section>

              <q-item-section side top>
                <div class="column items-end">
                  <q-badge :color="getStatusColor(item.status)" class="status-badge q-mb-xs">
                    {{ formatStatus(item.status) }}
                  </q-badge>
                  <div class="text-caption text-grey-7">
                    {{ item.tanggal_singkat }}
                  </div>
                  <div class="text-caption text-grey-7">
                    {{ item.waktu }}
                  </div>
                  <div v-if="item.tipe === 'transaksi'" class="text-caption text-grey-7 q-mt-xs">
                    {{ item.metode_bayar }}
                  </div>
                </div>
              </q-item-section>
            </q-item>
          </q-list>
        </div>

        <!-- Pagination -->
        <div v-if="filteredRiwayat.length > itemsPerPage" class="q-mt-lg">
          <div class="row justify-between items-center">
            <div class="col">
              <div class="text-caption text-grey-7">
                Menampilkan {{ startIndex + 1 }}-{{ endIndex }} dari
                {{ filteredRiwayat.length }} data
              </div>
            </div>
            <div class="col-auto">
              <q-pagination
                v-model="currentPage"
                :max="totalPages"
                :max-pages="6"
                direction-links
                boundary-links
                color="primary"
                active-color="primary"
                active-text-color="white"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Dialog -->
    <q-dialog v-model="detailDialog" position="bottom">
      <q-card style="width: 100%; max-height: 80vh">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">
            Detail {{ selectedItem?.tipe === 'laporan' ? 'Laporan' : 'Transaksi' }}
          </div>
          <q-btn
            flat
            round
            dense
            icon="close"
            class="absolute-top-right"
            @click="detailDialog = false"
          />
        </q-card-section>

        <q-scroll-area style="height: calc(80vh - 100px)">
          <q-card-section v-if="selectedItem">
            <!-- Laporan Detail -->
            <div v-if="selectedItem.tipe === 'laporan'">
              <!-- Status & Info -->
              <!-- Status & Info -->
              <div class="row items-center q-mb-lg">
                <div class="col-auto">
                  <q-avatar
                    :color="getStatusColor(selectedItem.status)"
                    text-color="white"
                    size="60px"
                    class="shadow-2"
                  >
                    <q-icon :name="getStatusIcon(selectedItem.status)" size="28px" />
                  </q-avatar>
                </div>
                <div class="col q-ml-md">
                  <div class="text-h6 text-weight-bold">
                    {{ formatJumlahKarung(selectedItem) }} Sampah
                  </div>
                  <div>
                    <q-badge :color="getStatusColor(selectedItem.status)" class="q-mr-sm">
                      {{ formatStatus(selectedItem.status) }}
                    </q-badge>
                    <q-badge color="grey">
                      {{ selectedItem.estimasi_volume }}
                    </q-badge>
                  </div>
                </div>
              </div>

              <!-- Timeline -->
              <div class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Timeline</div>
                <div class="timeline">
                  <div class="timeline-item">
                    <div class="timeline-dot bg-primary"></div>
                    <div class="timeline-content">
                      <div class="text-weight-medium">Laporan dibuat</div>
                      <div class="text-caption text-grey-7">
                        {{ selectedItem.tanggal_lengkap }} {{ selectedItem.waktu }}
                      </div>
                    </div>
                  </div>
                  <div v-if="selectedItem.tanggal_verifikasi" class="timeline-item">
                    <div class="timeline-dot bg-blue"></div>
                    <div class="timeline-content">
                      <div class="text-weight-medium">Laporan diverifikasi</div>
                      <div class="text-caption text-grey-7">
                        {{ formatDateTime(selectedItem.tanggal_verifikasi) }}
                      </div>
                    </div>
                  </div>
                  <div v-if="selectedItem.tanggal_selesai" class="timeline-item">
                    <div class="timeline-dot bg-green"></div>
                    <div class="timeline-content">
                      <div class="text-weight-medium">Pengambilan selesai</div>
                      <div class="text-caption text-grey-7">
                        {{ formatDateTime(selectedItem.tanggal_selesai) }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Informasi Sampah -->
              <!-- Informasi Sampah -->
              <div class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Informasi Sampah</div>
                <q-card flat bordered>
                  <q-card-section>
                    <div class="row q-col-gutter-md">
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Jenis Sampah</div>
                        <div class="text-weight-medium">{{ selectedItem.jenis_sampah || '-' }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Estimasi Volume</div>
                        <div class="text-weight-medium">
                          {{ getDisplayJumlahKarung(selectedItem) }}
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Waktu Pengambilan</div>
                        <div class="text-weight-medium">
                          {{ selectedItem.waktu_pengambilan || '-' }}
                        </div>
                      </div>
                      <!-- Hapus jumlah karung untuk laporan karena sudah ada di estimasi volume -->
                      <div class="col-6" v-if="selectedItem.tipe === 'transaksi'">
                        <div class="text-caption text-grey-7">Jumlah Karung</div>
                        <div class="text-weight-medium">{{ selectedItem.total_karung || 0 }}</div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>

              <!-- Informasi Petugas -->
              <div class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Petugas</div>
                <q-card flat bordered>
                  <q-card-section>
                    <div v-if="selectedItem.petugas?.nama" class="row items-center">
                      <q-avatar color="blue" text-color="white" class="q-mr-sm">
                        {{ selectedItem.petugas.nama.charAt(0) }}
                      </q-avatar>
                      <div>
                        <div class="text-weight-medium">{{ selectedItem.petugas.nama }}</div>
                        <div class="text-caption text-grey-7">
                          {{ selectedItem.petugas.telp || 'Tidak ada telepon' }}
                        </div>
                      </div>
                    </div>
                    <div v-else class="text-center text-grey-6">
                      <q-icon name="person_off" size="40px" class="q-mb-sm" />
                      <div>Belum ada petugas yang ditugaskan</div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>

              <!-- Informasi Lokasi -->
              <div class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Lokasi Pengambilan</div>
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-caption">
                      <div class="row items-center q-mb-xs">
                        <q-icon name="location_on" size="14px" class="q-mr-xs" />
                        <span>{{ selectedItem.alamat || 'Tidak tersedia' }}</span>
                      </div>
                      <div class="row items-center">
                        <q-icon name="map" size="14px" class="q-mr-xs" />
                        <span>RT {{ selectedItem.rt || '-' }}/RW {{ selectedItem.rw || '-' }}</span>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>

              <!-- Foto Sampah -->
              <div v-if="selectedItem.foto_sampah" class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Foto Sampah</div>
                <q-card flat bordered>
                  <q-card-section class="text-center">
                    <img
                      :src="selectedItem.foto_sampah"
                      alt="Foto Sampah"
                      style="max-width: 100%; max-height: 200px; border-radius: 8px"
                    />
                  </q-card-section>
                </q-card>
              </div>

              <!-- Catatan -->
              <div v-if="selectedItem.catatan" class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Catatan</div>
                <q-card flat bordered>
                  <q-card-section>
                    {{ selectedItem.catatan }}
                  </q-card-section>
                </q-card>
              </div>

              <!-- Actions -->
              <div class="row q-gutter-sm">
                <q-btn
                  v-if="selectedItem.status === 'pending' || selectedItem.status === 'proses'"
                  label="Batalkan Laporan"
                  color="negative"
                  outline
                  @click="batalkanLaporan(selectedItem)"
                  class="col"
                />
                <q-btn
                  v-if="selectedItem.status === 'proses'"
                  label="Konfirmasi Selesai"
                  color="positive"
                  @click="konfirmasiSelesai(selectedItem)"
                  class="col"
                />
                <q-btn label="Tutup" color="primary" @click="detailDialog = false" class="col" />
              </div>
            </div>

            <!-- Transaksi Detail -->
            <!-- Di Detail Dialog untuk Transaksi -->
            <div v-else>
              <!-- Status & Info -->
              <div class="row items-center q-mb-lg">
                <div class="col-auto">
                  <q-avatar
                    :color="getStatusColor(selectedItem.status)"
                    text-color="white"
                    size="60px"
                    class="shadow-2"
                  >
                    <q-icon :name="getStatusIcon(selectedItem.status)" size="28px" />
                  </q-avatar>
                </div>
                <div class="col q-ml-md">
                  <div class="text-h6 text-weight-bold">
                    Rp {{ formatCurrency(selectedItem.jumlah) }}
                  </div>
                  <div>
                    <q-badge :color="getStatusColor(selectedItem.status)" class="q-mr-sm">
                      {{ formatStatus(selectedItem.status) }}
                    </q-badge>
                    <q-badge :color="selectedItem.jenis === 'pemasukan' ? 'green' : 'red'">
                      {{ selectedItem.jenis === 'pemasukan' ? 'Pemasukan' : 'Pengeluaran' }}
                    </q-badge>
                  </div>
                </div>
              </div>

              <!-- Informasi Transaksi -->
              <div class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Detail Transaksi</div>
                <q-card flat bordered>
                  <q-card-section>
                    <div class="row q-col-gutter-md">
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Jenis Transaksi</div>
                        <div class="text-weight-medium">{{ selectedItem.jenis_transaksi }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Metode Bayar</div>
                        <div class="text-weight-medium">{{ selectedItem.metode_bayar || '-' }}</div>
                      </div>
                      <!-- TAMPILKAN TOTAL_KARUNG UNTUK TRANSAKSI -->
                      <div class="col-6" v-if="selectedItem.tipe === 'transaksi'">
                        <div class="text-caption text-grey-7">Jumlah Karung</div>
                        <div class="text-weight-medium">
                          {{ selectedItem.total_karung || 0 }} karung
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Harga per Karung</div>
                        <div class="text-weight-medium">
                          Rp {{ formatCurrency(selectedItem.harga_per_karung) }}
                        </div>
                      </div>
                      <div class="col-12">
                        <div class="text-caption text-grey-7">Keterangan</div>
                        <div class="text-weight-medium">{{ selectedItem.catatan || '-' }}</div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>

              <!-- Informasi Petugas -->
              <div v-if="selectedItem.petugas?.nama" class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Petugas</div>
                <q-card flat bordered>
                  <q-card-section>
                    <div class="row items-center">
                      <q-avatar color="blue" text-color="white" class="q-mr-sm">
                        {{ selectedItem.petugas.nama.charAt(0) }}
                      </q-avatar>
                      <div>
                        <div class="text-weight-medium">{{ selectedItem.petugas.nama }}</div>
                        <div class="text-caption text-grey-7">
                          {{ selectedItem.petugas.telp || 'Tidak ada telepon' }}
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>

              <!-- Bukti Bayar -->
              <div v-if="selectedItem.bukti_bayar" class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Bukti Pembayaran</div>
                <q-card flat bordered>
                  <q-card-section class="text-center">
                    <img
                      :src="selectedItem.bukti_bayar"
                      alt="Bukti Bayar"
                      style="max-width: 100%; max-height: 200px; border-radius: 8px"
                    />
                  </q-card-section>
                </q-card>
              </div>

              <!-- Catatan -->
              <div v-if="selectedItem.catatan" class="q-mb-lg">
                <div class="text-subtitle1 text-weight-bold q-mb-sm">Catatan</div>
                <q-card flat bordered>
                  <q-card-section>
                    {{ selectedItem.catatan }}
                  </q-card-section>
                </q-card>
              </div>

              <!-- Actions -->
              <div class="row q-gutter-sm">
                <q-btn label="Tutup" color="primary" @click="detailDialog = false" class="col" />
              </div>
            </div>
          </q-card-section>
        </q-scroll-area>
      </q-card>
    </q-dialog>

    <!-- Export Dialog -->
    <q-dialog v-model="exportDialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Export Data</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-radio v-model="exportFormat" val="excel" label="Excel (.xlsx)" />
          <q-radio v-model="exportFormat" val="pdf" label="PDF (.pdf)" />
          <q-radio v-model="exportFormat" val="csv" label="CSV (.csv)" />

          <div class="q-mt-md">
            <div class="text-caption text-grey-7 q-mb-xs">Rentang Tanggal</div>
            <div class="row q-col-gutter-sm">
              <div class="col-12 col-sm-6">
                <q-input v-model="exportStartDate" label="Dari" dense outlined type="date" />
              </div>
              <div class="col-12 col-sm-6">
                <q-input
                  v-model="exportEndDate"
                  label="Sampai"
                  dense
                  outlined
                  type="date"
                  :min="exportStartDate"
                />
              </div>
            </div>
          </div>

          <div class="q-mt-md">
            <div class="text-caption text-grey-7 q-mb-xs">Jenis Data</div>
            <q-radio v-model="exportTipe" val="all" label="Semua Data" />
            <q-radio v-model="exportTipe" val="laporan" label="Laporan Saja" />
            <q-radio v-model="exportTipe" val="transaksi" label="Transaksi Saja" />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Batal" color="grey" @click="exportDialog = false" />
          <q-btn label="Export" color="primary" @click="doExport" :loading="exporting" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Notification Toast -->
    <q-dialog v-model="showNotification" position="top">
      <q-card style="width: 350px">
        <q-card-section class="row items-center">
          <q-avatar :icon="notificationIcon" :color="notificationColor" text-color="white" />
          <span class="q-ml-sm">{{ notificationMessage }}</span>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import axios from 'axios'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const router = useRouter()

// State utama
const semuaRiwayat = ref([])
const opsiBulan = ref([])
const loading = ref(false)
const loadingBulan = ref(false)
const error = ref(false)
const errorMessage = ref('')
const saldo = ref(0)

// Filter state
const bulanDipilih = ref('')
const searchQuery = ref('')
const tipeFilter = ref('')
const statusFilter = ref([])
const minKarung = ref(null)
const maxKarung = ref(null)
const startDate = ref('')
const endDate = ref('')
const showAdvancedFilters = ref(false)

// UI state
const viewMode = ref('list')
const detailDialog = ref(false)
const selectedItem = ref(null)
const exportDialog = ref(false)
const exportFormat = ref('excel')
const exportTipe = ref('all')
const exporting = ref(false)
const exportStartDate = ref('')
const exportEndDate = ref('')
const showNotification = ref(false)
const notificationMessage = ref('')
const notificationIcon = ref('')
const notificationColor = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Stats
const stats = ref({
  laporan: {
    total: 0,
    menunggu: 0,
    diproses: 0,
    totalKarung: 0,
    statusStats: {},
  },
  transaksi: {
    total: 0,
    pemasukan: 0,
    pengeluaran: 0,
    totalKarung: 0,
    jenisStats: {},
  },
})

// Options
const tipeOptions = [
  { label: 'Semua Data', value: '' },
  { label: 'Laporan Sampah', value: 'laporan' },
  { label: 'Transaksi', value: 'transaksi' },
]

const statusOptions = [
  { label: 'Menunggu', value: 'pending' },
  { label: 'Diproses', value: 'proses' },
  { label: 'Selesai', value: 'selesai' },
  { label: 'Ditolak', value: 'ditolak' },
]

// Helper functions
const getAuthHeaders = () => {
  const token = localStorage.getItem('token') || ''
  return {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  }
}

const formatCurrency = (amount) => {
  if (!amount) return '0'
  return new Intl.NumberFormat('id-ID').format(amount)
}

const formatDateTime = (datetimeStr) => {
  if (!datetimeStr) return ''
  try {
    const date = new Date(datetimeStr)
    return date.toLocaleString('id-ID', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return ''
  }
}

const formatStatus = (status) => {
  const statusMap = {
    pending: 'Menunggu',
    proses: 'Diproses',
    selesai: 'Selesai',
    ditolak: 'Ditolak',
    menunggu: 'Menunggu',
    diproses: 'Diproses',
    diverifikasi: 'Diverifikasi',
    dibatalkan: 'Dibatalkan',
  }
  return statusMap[status] || status
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

// Status helpers
const getStatusColor = (status) => {
  const statusMap = {
    pending: 'orange',
    proses: 'blue',
    selesai: 'positive',
    ditolak: 'negative',
    menunggu: 'orange',
    diproses: 'blue',
    diverifikasi: 'cyan',
    dibatalkan: 'negative',
    lunas: 'positive',
    gagal: 'negative',
  }
  return statusMap[status] || 'grey'
}

const getStatusIcon = (status) => {
  const iconMap = {
    pending: 'schedule',
    proses: 'pending_actions',
    selesai: 'check_circle',
    ditolak: 'cancel',
    menunggu: 'schedule',
    diproses: 'pending_actions',
    diverifikasi: 'verified',
    dibatalkan: 'cancel',
    lunas: 'check_circle',
    gagal: 'error',
  }
  return iconMap[status] || 'help'
}

const getTipeColor = (tipe) => {
  return tipe === 'laporan' ? 'primary' : 'teal'
}

const getTipeIcon = (tipe) => {
  return tipe === 'laporan' ? 'description' : 'payments'
}

const getCardClass = (item) => {
  if (item.tipe === 'transaksi') {
    return item.jenis === 'pemasukan' ? 'card-pemasukan' : 'card-pengeluaran'
  }
  return ''
}

const getListItemClass = (item) => {
  if (item.tipe === 'transaksi') {
    return item.jenis === 'pemasukan' ? 'item-pemasukan' : 'item-pengeluaran'
  }
  return ''
}

const getTextColor = (item) => {
  if (item.tipe === 'transaksi') {
    return item.jenis === 'pemasukan' ? 'text-green' : 'text-red'
  }
  return 'text-primary'
}

// Load data functions
const loadDaftarBulan = async () => {
  loadingBulan.value = true
  try {
    const res = await axios.get(
      'https://spsbackend.pythonanywhere.com/api/riwayat/user/bulan-tersedia',
      {
        headers: getAuthHeaders(),
      },
    )

    if (res.data.success) {
      // TAMBAHKAN field 'value' yang sama dengan 'bulan_tahun'
      opsiBulan.value = res.data.data.map((item) => ({
        ...item,
        value: item.bulan_tahun, // INI YANG PERLU DITAMBAH
      }))

      // Set default to current month if exists
      const currentMonth = opsiBulan.value.find((b) => b.isCurrent)
      bulanDipilih.value = currentMonth ? currentMonth.value : opsiBulan.value[0]?.value || ''
    }
  } catch (error) {
    console.error('Error loading bulan:', error)

    // Fallback
    const currentDate = new Date()
    const namaBulan = [
      'Januari',
      'Februari',
      'Maret',
      'April',
      'Mei',
      'Juni',
      'Juli',
      'Agustus',
      'September',
      'Oktober',
      'November',
      'Desember',
    ]

    opsiBulan.value = [
      {
        bulan_tahun: `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}`,
        value: `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}`, // INI JUGA
        label: `${namaBulan[currentDate.getMonth()]} ${currentDate.getFullYear()}`,
        count: 0,
        isCurrent: true,
      },
    ]

    bulanDipilih.value = opsiBulan.value[0].value
  } finally {
    loadingBulan.value = false
  }
}

const loadRiwayat = async () => {
  loading.value = true
  error.value = false
  try {
    const params = {}

    // PERBAIKI: Hanya kirim value bulan, bukan object
    if (bulanDipilih.value) {
      // Pastikan bulanDipilih adalah string 'YYYY-MM', bukan object
      params.bulan =
        typeof bulanDipilih.value === 'object'
          ? bulanDipilih.value.value // Jika object, ambil value-nya
          : bulanDipilih.value // Jika string, pakai langsung
    }

    if (tipeFilter.value) params.tipe = tipeFilter.value

    console.log('Param yang dikirim:', params) // Debug

    const res = await axios.get('https://spsbackend.pythonanywhere.com/api/riwayat/user', {
      params,
      headers: getAuthHeaders(),
    })

    if (res.data.success) {
      semuaRiwayat.value = res.data.data
      await loadStats()
      await loadSaldo()
      showNotificationFn('positive', 'Data berhasil dimuat', 'check_circle')
    } else {
      throw new Error(res.data.message || 'Gagal memuat riwayat')
    }
  } catch (error) {
    console.error('Error loading riwayat:', error)
    error.value = true
    errorMessage.value = error.message
    showNotificationFn('negative', 'Gagal memuat data riwayat', 'error')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const params = {}
    if (bulanDipilih.value) {
      // SAMA: Hanya kirim string bulan
      params.bulan =
        typeof bulanDipilih.value === 'object' ? bulanDipilih.value.value : bulanDipilih.value
    }

    console.log('Param stats:', params) // Debug

    const res = await axios.get('https://spsbackend.pythonanywhere.com/api/riwayat/user/stats', {
      params,
      headers: getAuthHeaders(),
    })

    if (res.data.success) {
      stats.value = res.data.data
    }
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

watch(
  bulanDipilih,
  (newVal) => {
    console.log('bulanDipilih berubah:', newVal)
    console.log('Tipe:', typeof newVal)
  },
  { immediate: true },
)

const loadSaldo = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    const res = await axios.get(
      `https://spsbackend.pythonanywhere.com/api/warga/by-user/${userId}`,
      {
        headers: getAuthHeaders(),
      },
    )

    if (res.data.success) {
      saldo.value = parseFloat(res.data.data.saldo) || 0
    }
  } catch (error) {
    console.error('Error loading saldo:', error)
  }
}

// Filter functions
const applyAdvancedFilters = () => {
  currentPage.value = 1
  showAdvancedFilters.value = false
}

const resetFilters = () => {
  searchQuery.value = ''
  tipeFilter.value = ''
  statusFilter.value = []
  minKarung.value = null
  maxKarung.value = null
  startDate.value = ''
  endDate.value = ''
  currentPage.value = 1
  showAdvancedFilters.value = false
}

// Computed properties
const filteredRiwayat = computed(() => {
  let filtered = [...semuaRiwayat.value]

  // Search filter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(
      (item) =>
        (item.kode || '').toLowerCase().includes(query) ||
        (item.jenis || '').toLowerCase().includes(query) ||
        (item.catatan || '').toLowerCase().includes(query) ||
        (item.petugas?.nama || '').toLowerCase().includes(query) ||
        String(item.jumlah_karung).includes(query) ||
        String(item.jumlah).includes(query),
    )
  }

  // Status filter
  if (statusFilter.value.length > 0) {
    filtered = filtered.filter((item) => statusFilter.value.includes(item.status))
  }

  // Karung count filter (only for laporan)
  if (minKarung.value !== null) {
    filtered = filtered.filter((item) => {
      if (item.tipe !== 'laporan') return true
      return item.jumlah_karung >= minKarung.value
    })
  }
  if (maxKarung.value !== null) {
    filtered = filtered.filter((item) => {
      if (item.tipe !== 'laporan') return true
      return item.jumlah_karung <= maxKarung.value
    })
  }

  // Date range filter
  if (startDate.value) {
    filtered = filtered.filter((item) => {
      if (!item.tanggal) return true
      const itemDate = new Date(item.tanggal).toISOString().split('T')[0]
      return itemDate >= startDate.value
    })
  }
  if (endDate.value) {
    filtered = filtered.filter((item) => {
      if (!item.tanggal) return true
      const itemDate = new Date(item.tanggal).toISOString().split('T')[0]
      return itemDate <= endDate.value
    })
  }

  return filtered
})

const totalKarung = computed(() => {
  // Hanya hitung dari transaksi, bukan dari laporan
  return filteredRiwayat.value
    .filter((item) => item.tipe === 'transaksi' && item.total_karung)
    .reduce((total, item) => total + (parseInt(item.total_karung) || 0), 0)
})

const tampilJudulBulan = computed(() => {
  if (!bulanDipilih.value) return 'Semua Riwayat'
  const [tahun, bulan] = bulanDipilih.value.split('-')
  const namaBulan = [
    'Januari',
    'Februari',
    'Maret',
    'April',
    'Mei',
    'Juni',
    'Juli',
    'Agustus',
    'September',
    'Oktober',
    'November',
    'Desember',
  ]
  return `${namaBulan[parseInt(bulan) - 1]} ${tahun}`
})

// Pagination computed
const totalPages = computed(() => Math.ceil(filteredRiwayat.value.length / itemsPerPage.value))
const paginatedRiwayat = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredRiwayat.value.slice(start, end)
})
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value)
const endIndex = computed(() =>
  Math.min(startIndex.value + itemsPerPage.value, filteredRiwayat.value.length),
)

// Event handlers
const handleBulanChange = () => {
  currentPage.value = 1
  loadRiwayat()
}

const showDetail = (item) => {
  // Load detail data based on type
  if (item.tipe === 'laporan') {
    loadLaporanDetail(item.id)
  } else {
    loadTransaksiDetail(item.id)
  }
}

// Tambahkan fungsi helper
const formatJumlahKarung = (item) => {
  if (item.tipe === 'laporan') {
    // Untuk laporan, tampilkan estimasi_volume (sedikit/sedang/banyak)
    return item.estimasi_volume || 'Tidak ada estimasi'
  } else if (item.tipe === 'transaksi') {
    // Untuk transaksi, tampilkan angka total_karung
    return item.total_karung ? `${item.total_karung} karung` : 'Tidak ada karung'
  }
  return 'Tidak ada data'
}

// Untuk tampilkan dalam jumlah
const getDisplayJumlahKarung = (item) => {
  if (item.tipe === 'laporan') {
    // Mapping teks estimasi_volume ke deskripsi
    const estimasiMap = {
      sedikit: 'Sedikit (1-2 kantong)',
      sedang: 'Sedang (3-5 kantong)',
      banyak: 'Banyak (6+ kantong)',
    }
    return estimasiMap[item.estimasi_volume] || item.estimasi_volume || 'Tidak ada estimasi'
  } else if (item.tipe === 'transaksi') {
    return item.total_karung ? `${item.total_karung} karung` : '-'
  }
  return '-'
}

const loadLaporanDetail = async (id) => {
  try {
    const res = await axios.get(`https://spsbackend.pythonanywhere.com/api/riwayat/laporan/${id}`, {
      headers: getAuthHeaders(),
    })

    if (res.data.success) {
      selectedItem.value = res.data.data
      detailDialog.value = true
    }
  } catch (error) {
    console.error('Error loading laporan detail:', error)
    showNotificationFn('negative', 'Gagal memuat detail laporan', 'error')
  }
}

const loadTransaksiDetail = async (id) => {
  try {
    const res = await axios.get(
      `https://spsbackend.pythonanywhere.com/api/riwayat/transaksi/${id}`,
      {
        headers: getAuthHeaders(),
      },
    )

    if (res.data.success) {
      selectedItem.value = res.data.data
      detailDialog.value = true
    }
  } catch (error) {
    console.error('Error loading transaksi detail:', error)
    showNotificationFn('negative', 'Gagal memuat detail transaksi', 'error')
  }
}

const createLaporan = () => {
  router.push('/laporan/baru')
}

const batalkanLaporan = async (item) => {
  $q.dialog({
    title: 'Konfirmasi',
    message: 'Apakah Anda yakin ingin membatalkan laporan ini?',
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const res = await axios.put(
        `https://spsbackend.pythonanywhere.com/api/riwayat/laporan/${item.id}/batal`,
        {},
        {
          headers: getAuthHeaders(),
        },
      )

      if (res.data.success) {
        showNotificationFn('positive', 'Laporan berhasil dibatalkan', 'check_circle')
        loadRiwayat()
        detailDialog.value = false
      }
    } catch {
      showNotificationFn('negative', 'Gagal membatalkan laporan', 'error')
    }
  })
}

const konfirmasiSelesai = async (item) => {
  $q.dialog({
    title: 'Konfirmasi',
    message: 'Apakah Anda yakin pengambilan sudah selesai?',
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      const res = await axios.put(
        `https://spsbackend.pythonanywhere.com/api/riwayat/laporan/${item.id}/selesai`,
        {
          catatan: 'Dikonfirmasi selesai oleh user',
        },
        {
          headers: getAuthHeaders(),
        },
      )

      if (res.data.success) {
        showNotificationFn('positive', 'Laporan dikonfirmasi selesai', 'check_circle')
        loadRiwayat()
        detailDialog.value = false
      }
    } catch {
      showNotificationFn('negative', 'Gagal mengkonfirmasi laporan', 'error')
    }
  })
}

// Export function
const doExport = async () => {
  exporting.value = true
  try {
    const params = {
      format: exportFormat.value,
      tipe: exportTipe.value,
    }

    if (exportStartDate.value) params.start_date = exportStartDate.value
    if (exportEndDate.value) params.end_date = exportEndDate.value
    if (bulanDipilih.value) params.bulan = bulanDipilih.value

    // Note: You'll need to implement the export endpoint
    // const res = await axios.get('https://spsbackend.pythonanywhere.com/api/riwayat/export', {
    //   params,
    //   headers: getAuthHeaders(),
    //   responseType: 'blob'
    // })

    // For now, show success message
    showNotificationFn('positive', 'Fitur export akan segera tersedia', 'info')
    exportDialog.value = false
  } catch {
    showNotificationFn('negative', 'Gagal mengexport data', 'error')
  } finally {
    exporting.value = false
  }
}

// Notification helper
const showNotificationFn = (type, message, icon) => {
  notificationColor.value = type
  notificationMessage.value = message
  notificationIcon.value = icon
  showNotification.value = true

  setTimeout(() => {
    showNotification.value = false
  }, 3000)
}

// Watch for changes
watch([searchQuery, tipeFilter, statusFilter], () => {
  currentPage.value = 1
})

// Lifecycle
onMounted(async () => {
  await loadDaftarBulan()
  await loadRiwayat()
})
</script>

<style scoped>
/* Header Gradient */
.header-gradient {
  background: linear-gradient(135deg, #006837 0%, #4caf50 100%);
  border-radius: 0 0 24px 24px;
}

/* Stats Card */
.stats-card {
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
}

/* Filter Card */
.filter-card {
  border-radius: 16px;
  border: 1px solid rgba(0, 104, 55, 0.1);
}

/* Riwayat Cards */
.riwayat-grid-card {
  border-radius: 16px;
  border: 1px solid rgba(0, 104, 55, 0.1);
  transition: all 0.3s ease;
}

.riwayat-grid-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 104, 55, 0.15);
  border-color: #4caf50;
}

.card-pemasukan {
  border-left: 4px solid #4caf50;
}

.card-pengeluaran {
  border-left: 4px solid #f44336;
}

.riwayat-list-item {
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.riwayat-list-item:hover {
  background: rgba(76, 175, 80, 0.05);
  border-color: #4caf50;
  transform: translateX(5px);
}

.item-pemasukan:hover {
  background: rgba(76, 175, 80, 0.1);
  border-color: #4caf50;
}

.item-pengeluaran:hover {
  background: rgba(244, 67, 54, 0.1);
  border-color: #f44336;
}

/* Status Badge */
.status-badge {
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.tipe-badge {
  border-radius: 10px;
  padding: 2px 8px;
  font-size: 10px;
  font-weight: 500;
}

/* Illustration */
.illustration-container {
  position: relative;
  display: inline-block;
}

.floating-icon {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: white;
  border-radius: 50%;
  padding: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 9px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e0e0e0;
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.timeline-dot {
  position: absolute;
  left: -30px;
  top: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timeline-content {
  padding-left: 10px;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .header-gradient {
    border-radius: 0 0 20px 20px;
  }

  .text-h4 {
    font-size: 1.5rem;
  }

  .riwayat-grid-card {
    margin-bottom: 16px;
  }

  .status-badge {
    font-size: 10px;
    padding: 3px 8px;
  }
}

/* Transaction specific styles */
.text-green {
  color: #4caf50 !important;
}

.text-red {
  color: #f44336 !important;
}
</style>
