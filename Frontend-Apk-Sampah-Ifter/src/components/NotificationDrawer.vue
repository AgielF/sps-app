<template>
  <q-drawer
    :model-value="modelValue"
    side="right"
    overlay
    behavior="mobile"
    @update:model-value="$emit('update:modelValue', $event)"
    class="notification-drawer"
  >
    <q-toolbar class="bg-primary text-white shadow-3 header-drawer">
      <q-toolbar-title class="text-weight-bold">Notifikasi</q-toolbar-title>
      <q-btn icon="close" flat round dense @click="$emit('update:modelValue', false)" />
    </q-toolbar>
    
    <q-list separator class="q-pt-sm">
      <q-item-label header class="text-weight-bold text-grey-8">Aktivitas Terbaru (4)</q-item-label>
      
      <q-item clickable v-ripple class="notification-item">
        <q-item-section avatar>
          <q-avatar icon="calendar_today" color="cyan-1" text-color="cyan-8" />
        </q-item-section>
        <q-item-section>
          <q-item-label class="text-weight-medium">Jadwal Pengambilan Besok</q-item-label>
          <q-item-label caption>Petugas [Nama] akan menjemput sampah pukul 08.00.</q-item-label>
        </q-item-section>
        <q-item-section side>
            <q-item-label caption>10m</q-item-label>
        </q-item-section>
      </q-item>
      
      <q-item clickable v-ripple class="notification-item">
        <q-item-section avatar>
          <q-avatar icon="check_circle" color="green-1" text-color="green-8" />
        </q-item-section>
        <q-item-section>
          <q-item-label class="text-weight-medium">Sampah Berhasil Dijemput</q-item-label>
          <q-item-label caption>Transaksi #TRX-20231026 telah selesai dicatat.</q-item-label>
        </q-item-section>
        <q-item-section side>
            <q-item-label caption>1j</q-item-label>
        </q-item-section>
      </q-item>
      
      <q-item clickable v-ripple class="notification-item">
        <q-item-section avatar>
          <q-avatar icon="wallet" color="orange-1" text-color="orange-8" />
        </q-item-section>
        <q-item-section>
          <q-item-label class="text-weight-medium">Saldo Tertambah!</q-item-label>
          <q-item-label caption>Pemasukan sebesar Rp 15.000 telah masuk ke kas.</q-item-label>
        </q-item-section>
        <q-item-section side>
            <q-item-label caption>1h</q-item-label>
        </q-item-section>
      </q-item>
      
      <q-item clickable v-ripple class="notification-item">
        <q-item-section avatar>
          <q-avatar icon="person_add" color="blue-1" text-color="blue-8" />
        </q-item-section>
        <q-item-section>
          <q-item-label class="text-weight-medium">Pendaftaran User Baru</q-item-label>
          <q-item-label caption>User 'Dani' baru saja mendaftar. Perlu verifikasi.</q-item-label>
        </q-item-section>
        <q-item-section side>
            <q-item-label caption>2j</q-item-label>
        </q-item-section>
      </q-item>
      
    </q-list>
    
    <q-item clickable class="absolute-bottom bg-grey-2 text-center text-primary text-weight-medium q-py-md footer-link">
        <q-item-section>Lihat Semua</q-item-section>
    </q-item>
    
  </q-drawer>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  modelValue: Boolean
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.notification-drawer {
    width: 300px;
    background-color: #f7fcf7;
}
.bg-primary {
    background-color: #006837 !important;
}
.header-drawer {
    border-bottom: 3px solid #FFC107;
}

.notification-item {
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
}

.q-item-section--avatar {
    padding-right: 12px;
}

.footer-link {
    border-top: 1px solid #ddd;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.05); 
}
</style>