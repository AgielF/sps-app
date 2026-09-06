// src/stores/laporanStore.js
import { ref } from 'vue'

// Data reaktif untuk menyimpan pengajuan
export const jadwalPengajuan = ref('')
export const jenisSampahPengajuan = ref('')
export const statusPengajuan = ref(false)

// Fungsi untuk set pengajuan
export const setPengajuan = (jadwal, jenisSampah) => {
  jadwalPengajuan.value = jadwal
  jenisSampahPengajuan.value = jenisSampah
  statusPengajuan.value = true
}

// Fungsi untuk clear pengajuan
export const clearPengajuan = () => {
  jadwalPengajuan.value = ''
  jenisSampahPengajuan.value = ''
  statusPengajuan.value = false
}