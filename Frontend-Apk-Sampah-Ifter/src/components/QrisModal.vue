<template>
  <q-card style="width: 300px; max-width: 90vw; border-radius: 16px;">
    <q-card-section class="q-pa-lg text-center">
      <div class="text-left text-h6 text-green-9 text-weight-bold" style="line-height: 1.2;">
          Silahkan Scan dan<br>Lakukan Pembayaran
      </div>
      <div class="text-left text-h6 text-green-9 text-weight-bold q-mb-md">
          Rp. {{ amount }}
      </div>

      <div class="qr-placeholder q-mb-md">
          <img src="https://via.placeholder.com/250x350/FFFFFF/333333?text=QRIS+EDU+PARTNER" alt="QRIS Code" style="width: 100%; height: auto; border-radius: 8px; border: 1px solid #ddd;">
      </div>

      <q-btn 
        label="OK" 
        color="yellow-8" 
        text-color="black"
        unelevated 
        class="full-width text-weight-bold"
        @click="$emit('close')"
      />
    </q-card-section>
  </q-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

defineProps({
  amount: {
    type: String,
    default: '20.000'
  }
})

defineEmits(['close'])
</script>

<style scoped>
.qr-placeholder {
    background: #fff;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 200px;
}
.text-green-9 {
    color: #006837 !important;
}
</style>