<template>
  <q-page class="full-height q-pa-none">
    <!-- Header Title -->

    <!-- Map Container -->
    <div class="map-container">
      <div id="map" class="map-view"></div>
    </div>

    <!-- Map Info -->
    <div class="map-info absolute-bottom q-ma-md">
      <q-card flat bordered class="info-card">
        <q-card-section class="q-pa-md">
          <div class="row items-center q-gutter-sm">
            <q-icon name="location_on" color="primary" size="24px" />
            <div>
              <div class="text-body2 text-weight-bold text-primary">Lokasi Petugas</div>
              <div class="text-caption text-grey-7">{{ infoText }}</div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Refresh Button -->
    <q-page-sticky position="top-right" :offset="[18, 70]">
      <q-btn fab icon="refresh" color="primary" @click="refreshData" class="shadow-2" />
    </q-page-sticky>

    <!-- Location Button -->
    <q-page-sticky position="bottom-right" :offset="[18, 100]">
      <q-btn fab icon="my_location" color="primary" @click="centerMap" class="shadow-2" />
    </q-page-sticky>

    <!-- Loading Dialog -->
    <q-dialog v-model="loading" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-spinner color="primary" size="3em" />
          <q-space />
          <span class="text-h6">Memuat data...</span>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// FIX leaflet icon
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

export default {
  data() {
    return {
      map: null,
      markers: [],
      loading: false,
      infoText: 'Menunggu data...',
      currentLocation: null,
      watchId: null,
    }
  },

  async mounted() {
    this.initMap()
    this.initCurrentLocation()
    await this.loadData()

    // Refresh tile layer
    setTimeout(() => {
      if (this.map) {
        this.map.invalidateSize()
      }
    }, 500)
  },

  beforeUnmount() {
    // Cleanup geolocation watcher
    if (this.watchId !== null) {
      navigator.geolocation.clearWatch(this.watchId)
    }
  },

  methods: {
    initMap() {
      // Default view ke Indonesia
      this.map = L.map('map').setView([-2.5489, 118.0149], 5)

      // Add tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors',
      }).addTo(this.map)
    },

    initCurrentLocation() {
      if ('geolocation' in navigator) {
        // Get current position once
        navigator.geolocation.getCurrentPosition(
          (position) => {
            this.currentLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            }
            this.addCurrentLocationMarker()
          },
          (error) => {
            console.error('Error getting location:', error)
            this.infoText = 'Tidak dapat mengakses lokasi saat ini'
          },
        )

        // Watch for location changes
        this.watchId = navigator.geolocation.watchPosition(
          (position) => {
            this.currentLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            }
            this.updateCurrentLocationMarker()
          },
          (error) => {
            console.error('Error watching location:', error)
          },
          {
            enableHighAccuracy: true,
            maximumAge: 10000,
            timeout: 5000,
          },
        )
      } else {
        this.infoText = 'Browser tidak mendukung geolocation'
      }
    },

    addCurrentLocationMarker() {
      if (this.currentLocation) {
        // Custom icon for current location
        const currentLocationIcon = L.divIcon({
          className: 'current-location-marker',
          html: '<div class="pulse-dot"></div>',
          iconSize: [20, 20],
          iconAnchor: [10, 10],
        })

        // Add marker for current location
        const marker = L.marker([this.currentLocation.lat, this.currentLocation.lng], {
          icon: currentLocationIcon,
          zIndexOffset: 1000,
        })
          .addTo(this.map)
          .bindPopup('<b>Lokasi Anda Saat Ini</b>')

        this.markers.push(marker)
      }
    },

    updateCurrentLocationMarker() {
      // Remove existing current location markers
      this.markers = this.markers.filter((marker) => {
        if (marker.options.icon?.options?.className === 'current-location-marker') {
          this.map.removeLayer(marker)
          return false
        }
        return true
      })

      // Add updated marker
      this.addCurrentLocationMarker()
    },

    async loadData() {
      this.loading = true
      try {
        // Clear existing markers
        this.clearMarkers()

        // Fetch data from API
        const lokasi = await this.fetchLokasi()

        if (lokasi && lokasi.length > 0) {
          this.addAllMarkers(lokasi)
          this.infoText = `${lokasi.length} petugas ditemukan`

          // Fit bounds to show all markers
          if (this.markers.length > 1) {
            const group = new L.featureGroup(this.markers)
            this.map.fitBounds(group.getBounds().pad(0.1))
          } else if (this.markers.length === 1) {
            this.map.setView(this.markers[0].getLatLng(), 15)
          }
        } else {
          this.infoText = 'Tidak ada data petugas'
        }
      } catch (error) {
        console.error('Error loading data:', error)
        this.infoText = 'Gagal memuat data petugas'
      } finally {
        this.loading = false
      }
    },

    async fetchLokasi() {
      try {
        // Get token from localStorage or wherever you store it
        const token = localStorage.getItem('token') || ''

        const res = await fetch('https://spsbackend.pythonanywhere.com/api/lokasi/petugas', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }

        const json = await res.json()

        if (json.success) {
          return json.data
        } else {
          throw new Error(json.message || 'Failed to fetch data')
        }
      } catch (error) {
        console.error('Fetch error:', error)
        throw error
      }
    },

    addAllMarkers(data) {
      console.log('DATA LIVE:', data)
      const petugasIcon = L.icon({
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
      })

      data.forEach((p) => {
        if (
          !p.live_latitude ||
          !p.live_longitude ||
          p.live_latitude === 0 ||
          p.live_longitude === 0
        ) {
          console.warn('Invalid live location:', p)
          return
        }

        const lat = parseFloat(p.live_latitude)
        const lng = parseFloat(p.live_longitude)

        const marker = L.marker([lat, lng], { icon: petugasIcon }).addTo(this.map).bindPopup(`
        <div style="min-width: 200px">
          <b>${p.nama_lengkap}</b><br>
          <small>Telepon: ${p.no_telepon || '-'}</small><br>
        </div>
      `)

        this.markers.push(marker)
      })
    },
    clearMarkers() {
      this.markers.forEach((marker) => {
        if (this.map.hasLayer(marker)) {
          this.map.removeLayer(marker)
        }
      })
      this.markers = []
    },

    centerMap() {
      if (this.currentLocation) {
        this.map.setView([this.currentLocation.lat, this.currentLocation.lng], 15)
      } else if (this.markers.length > 0) {
        this.map.setView(this.markers[0].getLatLng(), 15)
      } else {
        // Default to Indonesia center
        this.map.setView([-2.5489, 118.0149], 5)
      }
    },

    async refreshData() {
      await this.loadData()
    },
  },
}
</script>

<style scoped>
.text-primary {
  color: #08602e !important;
}

.map-container {
  position: relative;
  height: calc(100vh - 56px);
}

#map {
  width: 100%;
  height: 100%;
}

.map-info {
  z-index: 1000;
  left: 0;
  right: 0;
  margin: 0 auto;
  max-width: calc(100% - 32px);
}

.info-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(8, 96, 46, 0.2);
}

:deep(.q-btn.bg-primary) {
  background: #08602e !important;
}

:deep(.q-btn.bg-primary:hover) {
  background: #0a7838 !important;
}

.full-height {
  height: 100vh;
  overflow: hidden;
}

.map-view {
  width: 100%;
  height: 100%;
}

.map-info {
  bottom: 70px !important;
  z-index: 999;
}

/* Custom styles for current location marker */
:deep(.current-location-marker) {
  background: none;
  border: none;
}

.pulse-dot {
  width: 20px;
  height: 20px;
  background-color: #2196f3;
  border-radius: 50%;
  box-shadow: 0 0 0 rgba(33, 150, 243, 0.4);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(33, 150, 243, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(33, 150, 243, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(33, 150, 243, 0);
  }
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .map-info {
    max-width: calc(100% - 16px);
    bottom: 80px !important;
  }

  .map-container {
    height: calc(100vh - 60px);
    margin-top: 60px;
  }
}
</style>
