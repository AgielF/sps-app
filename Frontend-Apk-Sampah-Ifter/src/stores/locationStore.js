import { defineStore } from 'pinia'
import api from 'src/services/api'

export const useLocationStore = defineStore('location', {
  state: () => ({
    isLive: false,
    watcherId: null,
    coords: null,

    // 🔥 TARUH DI SINI
    lastSentAt: 0,
  }),

  actions: {
    startTracking() {
      if (this.isLive) return

      this.watcherId = navigator.geolocation.watchPosition(
        async (pos) => {
          const now = Date.now()

          // ⏱️ THROTTLE 15 DETIK
          if (now - this.lastSentAt < 15000) return
          this.lastSentAt = now

          const coords = {
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            accuracy: pos.coords.accuracy,
          }

          this.coords = coords

          try {
            const token = localStorage.getItem('token')?.replace('Bearer ', '') || ''
            const petugasId = localStorage.getItem('petugas_id')
            if (!petugasId) return

            await api.post(
              '/api/petugas/update-location',
              {
                latitude: coords.latitude,
                longitude: coords.longitude,
                accuracy: coords.accuracy,
                speed: coords.speed,
                heading: coords.heading,
              },
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              },
            )

            console.log('📍 Lokasi terkirim ke database')
          } catch (err) {
            console.error('❌ Gagal kirim lokasi:', err.message)
          }
        },
        (err) => console.error('GPS error:', err),
        {
          enableHighAccuracy: true,
          maximumAge: 0,
          timeout: 10000,
        },
      )

      this.isLive = true
    },

    stopTracking() {
      if (this.watcherId) {
        navigator.geolocation.clearWatch(this.watcherId)
        this.watcherId = null
      }
      this.isLive = false
      this.lastSentAt = 0
    },
  },
})
