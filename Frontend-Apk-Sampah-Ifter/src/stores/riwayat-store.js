import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useRiwayatStore = defineStore('riwayat', () => {
  // State
  const riwayatList = ref([
    {
      id: 1,
      status: 'selesai',
      tanggal: '2025-04-15',
      jumlah: 2,
      jenisSampah: 'Sampah Organik',
      periode: 'april'
    },
    {
      id: 2,
      status: 'selesai',
      tanggal: '2025-04-08',
      jumlah: 1,
      jenisSampah: 'Sampah Plastik',
      periode: 'april'
    },
    {
      id: 3,
      status: 'selesai',
      tanggal: '2025-04-08',
      jumlah: 1,
      jenisSampah: 'Sampah Kertas',
      periode: 'april'
    },
    {
      id: 4,
      status: 'selesai',
      tanggal: '2025-05-08',
      jumlah: 3,
      jenisSampah: 'Sampah Campuran',
      periode: 'mei'
    },
    {
      id: 5,
      status: 'tertunda',
      tanggal: '2025-05-08',
      jumlah: 1,
      jenisSampah: 'Sampah Organik',
      periode: 'mei'
    },
    {
      id: 6,
      status: 'selesai',
      tanggal: '2025-05-08',
      jumlah: 2,
      jenisSampah: 'Sampah Plastik',
      periode: 'mei'
    }
  ])

  // Getters
  const getRiwayatByPeriode = computed(() => {
    return (periode) => riwayatList.value.filter(r => r.periode === periode)
  })

  const totalPengambilan = computed(() => {
    return riwayatList.value.length
  })

  const totalKarung = computed(() => {
    return riwayatList.value.reduce((total, r) => total + r.jumlah, 0)
  })

  // Actions
  function addRiwayat(riwayat) {
    const newRiwayat = {
      id: Date.now(),
      ...riwayat,
      createdAt: new Date().toISOString()
    }
    riwayatList.value.unshift(newRiwayat)
    return newRiwayat
  }

  function updateRiwayat(id, updates) {
    const index = riwayatList.value.findIndex(r => r.id === id)
    if (index !== -1) {
      riwayatList.value[index] = {
        ...riwayatList.value[index],
        ...updates
      }
    }
  }

  function deleteRiwayat(id) {
    const index = riwayatList.value.findIndex(r => r.id === id)
    if (index !== -1) {
      riwayatList.value.splice(index, 1)
    }
  }

  return {
    // State
    riwayatList,
    // Getters
    getRiwayatByPeriode,
    totalPengambilan,
    totalKarung,
    // Actions
    addRiwayat,
    updateRiwayat,
    deleteRiwayat
  }
})