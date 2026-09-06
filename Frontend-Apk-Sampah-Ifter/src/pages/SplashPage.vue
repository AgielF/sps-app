<template>
  <div class="splash-page flex flex-center fullscreen column">
    
    <img 
      src="../assets/Logo_SPS_BG-remove.png" 
      alt="Logo Suraja Peduli Sampah" 
      class="logo" 
    />
    
    <h5 class="app-title q-mt-md text-bold">
      Suraja Peduli Sampah.
    </h5>
    
    <q-spinner
      color="yellow-4"
      size="md"
      class="q-mt-xl"
    />
    
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const SPLASH_DURATION = 3000 // Durasi splash screen 3 detik

onMounted(() => {
  // Menunggu 3 detik lalu navigasi ke halaman login
  setTimeout(() => {
    router.push('/login')
  }, SPLASH_DURATION)
})
</script>

<style scoped>
/* 1. Kontainer Utama: Latar Belakang Gradien Halus */
.splash-page {
  /* Menggunakan gradien vertikal dari hijau tua ke hijau cerah untuk kesan futuristik */
  background: linear-gradient(160deg, #00513b 0%, #006837 50%, #008749 100%);
  color: #fff;
  overflow: hidden;
  /* Memastikan transisi yang halus jika ada elemen lain */
  transition: background 0.5s ease-in-out; 
}

/* 2. Style Logo */
.logo {
  width: 150px;
  height: auto;
  /* Animasi: Logo muncul dari bawah dan memudar masuk */
  animation: logo-fade-in 1.5s ease-out forwards;
  opacity: 0; /* Mulai tersembunyi */
  transform: translateY(20px);
}

/* 3. Style Teks */
.app-title {
  color: #FFC107; /* Kuning Emas/Amber untuk kontras futuristik */
  font-size: 28px;
  letter-spacing: 2px;
  /* Animasi: Teks muncul setelah logo */
  animation: title-fade-in 1.5s ease-out 0.5s forwards; /* Delay 0.5s */
  opacity: 0;
  transform: translateY(10px);
  /* Efek glow halus */
  text-shadow: 0 0 5px rgba(255, 193, 7, 0.4);
}

/* ================== KEYFRAMES ANIMASI ================== */

/* Animasi Fade In & Bounce untuk Logo */
@keyframes logo-fade-in {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
  }
  70% {
    opacity: 1;
    transform: translateY(-5px) scale(1.05); /* Sedikit memantul ke atas */
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Animasi Fade In untuk Judul */
@keyframes title-fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>