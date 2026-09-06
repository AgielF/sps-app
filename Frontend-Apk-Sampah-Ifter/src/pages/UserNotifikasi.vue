<template>
  <q-page class="bg-grey-2">
    <div class="q-pa-md">
      <!-- Header -->
<div class="text-h5 text-weight-bold q-mb-md text-dark-green">
  Notifikasi
</div>

      <!-- Notifikasi List -->
      <div class="notifications-list">
        <!-- Pengambilan Sampah -->
        <q-card flat class="notification-card q-mb-md" @click="showDetail('pengambilan')">
          <q-card-section class="row items-center q-pa-md">
            <div class="col-auto">
              <q-avatar size="50px" color="green-2">
                <q-icon name="local_shipping" color="green" size="28px" />
              </q-avatar>
            </div>
            <div class="col q-ml-md">
              <div class="text-subtitle1 text-weight-bold">
                Pengambilan Sampah
              </div>
              <div class="text-caption text-grey-7">
                Sampah akan diambil besok pagi
              </div>
            </div>
            <div class="col-auto text-right">
              <div class="text-caption text-grey-6">
                1 jam yang lalu
              </div>
              <q-icon name="chevron_right" color="grey-6" size="20px" />
            </div>
          </q-card-section>
        </q-card>

        <!-- Pembayaran Berhasil -->
        <q-card flat class="notification-card q-mb-md" @click="showDetail('pembayaran')">
          <q-card-section class="row items-center q-pa-md">
            <div class="col-auto">
              <q-avatar size="50px" color="yellow-2">
                <q-icon name="check_circle" color="yellow-8" size="28px" />
              </q-avatar>
            </div>
            <div class="col q-ml-md">
              <div class="text-subtitle1 text-weight-bold">
                Pembayaran Berhasil
              </div>
              <div class="text-caption text-grey-7">
                Pembayaran telah selesai
              </div>
            </div>
            <div class="col-auto text-right">
              <div class="text-caption text-grey-6">
                Kemarin
              </div>
              <q-icon name="chevron_right" color="grey-6" size="20px" />
            </div>
          </q-card-section>
        </q-card>

        <!-- Pengajuan Laporan Sampah -->
        <q-card flat class="notification-card q-mb-md" @click="showDetail('pengajuan')">
          <q-card-section class="row items-center q-pa-md">
            <div class="col-auto">
              <q-avatar size="50px" color="blue-2">
                <q-icon name="description" color="blue" size="28px" />
              </q-avatar>
            </div>
            <div class="col q-ml-md">
              <div class="text-subtitle1 text-weight-bold">
                Pengajuan Laporan Sampah
              </div>
              <div class="text-caption text-grey-7">
                Laporan sampah telah diajukan
              </div>
            </div>
            <div class="col-auto text-right">
              <div class="text-caption text-grey-6">
                Kemarin
              </div>
              <q-icon name="chevron_right" color="grey-6" size="20px" />
            </div>
          </q-card-section>
        </q-card>

        <!-- Pembayaran Belum Selesai -->
        <q-card flat class="notification-card q-mb-md" @click="showDetail('belum-bayar')">
          <q-card-section class="row items-center q-pa-md">
            <div class="col-auto">
              <q-avatar size="50px" color="red-2">
                <q-icon name="error" color="red" size="28px" />
              </q-avatar>
            </div>
            <div class="col q-ml-md">
              <div class="text-subtitle1 text-weight-bold">
                Pembayaran belum selesai
              </div>
              <div class="text-caption text-grey-7">
                Segera lakukan pembayaran
              </div>
            </div>
            <div class="col-auto text-right">
              <div class="text-caption text-grey-6">
                1 hari lalu
              </div>
              <q-icon name="chevron_right" color="grey-6" size="20px" />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Detail Dialog -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">Detail Notifikasi</div>
        </q-card-section>
        <q-card-section>
          {{ selectedNotification }}
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Tutup" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'UserNotifikasi',
  setup() {
    const showDialog = ref(false)
    const selectedNotification = ref('')

    const showDetail = (type) => {
      selectedNotification.value = `Detail notifikasi ${type}`
      showDialog.value = true
    }

    return {
      showDialog,
      selectedNotification,
      showDetail
    }
  }
}
</script>

<style scoped>
.notification-card {
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
    