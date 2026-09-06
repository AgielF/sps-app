import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useNotifikasiStore = defineStore('notifikasi', () => {
  // State
  const notifikasiList = ref([
    {
      id: 1,
      type: 'pengambilan',
      title: 'Pengambilan Sampah',
      message: 'Sampah akan diambil besok pagi',
      icon: 'local_shipping',
      iconColor: 'green',
      iconBgColor: 'green-2',
      timestamp: new Date(Date.now() - 3600000).toISOString(), // 1 jam lalu
      read: false
    },
    {
      id: 2,
      type: 'pembayaran',
      title: 'Pembayaran Berhasil',
      message: 'Pembayaran telah selesai',
      icon: 'check_circle',
      iconColor: 'yellow-8',
      iconBgColor: 'yellow-2',
      timestamp: new Date(Date.now() - 86400000).toISOString(), // Kemarin
      read: false
    },
    {
      id: 3,
      type: 'pengajuan',
      title: 'Pengajuan Laporan Sampah',
      message: 'Laporan sampah telah diajukan',
      icon: 'description',
      iconColor: 'blue',
      iconBgColor: 'blue-2',
      timestamp: new Date(Date.now() - 86400000).toISOString(), // Kemarin
      read: false
    },
    {
      id: 4,
      type: 'warning',
      title: 'Pembayaran belum selesai',
      message: 'Segera lakukan pembayaran',
      icon: 'error',
      iconColor: 'red',
      iconBgColor: 'red-2',
      timestamp: new Date(Date.now() - 172800000).toISOString(), // 2 hari lalu
      read: false
    }
  ])

  // Getters
  const unreadCount = computed(() => {
    return notifikasiList.value.filter(n => !n.read).length
  })

  const unreadNotifications = computed(() => {
    return notifikasiList.value.filter(n => !n.read)
  })

  // Actions
  function addNotifikasi(notifikasi) {
    const newNotifikasi = {
      id: Date.now(),
      ...notifikasi,
      timestamp: new Date().toISOString(),
      read: false
    }
    notifikasiList.value.unshift(newNotifikasi)
  }

  function markAsRead(id) {
    const notifikasi = notifikasiList.value.find(n => n.id === id)
    if (notifikasi) {
      notifikasi.read = true
    }
  }

  function markAllAsRead() {
    notifikasiList.value.forEach(n => {
      n.read = true
    })
  }

  function deleteNotifikasi(id) {
    const index = notifikasiList.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifikasiList.value.splice(index, 1)
    }
  }

  function clearAll() {
    notifikasiList.value = []
  }

  return {
    // State
    notifikasiList,
    // Getters
    unreadCount,
    unreadNotifications,
    // Actions
    addNotifikasi,
    markAsRead,
    markAllAsRead,
    deleteNotifikasi,
    clearAll
  }
})