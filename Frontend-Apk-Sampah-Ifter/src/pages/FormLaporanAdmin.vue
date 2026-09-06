<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="flex flex-center bg-green-1">
        
        <div class="content-wrapper" style="width: 90%; max-width: 400px;">
          <div class="text-center q-mb-lg">
            <h4 class="text-primary text-weight-bold q-my-none">Laporan Masalah</h4>
            <div class="text-grey-7">Jelaskan kendala Anda kepada Admin</div>
          </div>

          <q-card class="my-card shadow-3" style="border-radius: 16px;">
            <q-card-section>
              <q-form @submit="kirimLaporan" class="q-gutter-md">
                
                <q-input 
                  v-model="nama" 
                  outlined 
                  label="Nama Lengkap" 
                  bg-color="white"
                  dense
                  :rules="[val => !!val || 'Nama harus diisi']"
                >
                  <template v-slot:prepend>
                    <q-icon name="person" color="primary" />
                  </template>
                </q-input>

                <q-input 
                  v-model="kontak" 
                  outlined 
                  label="No. WhatsApp / Email" 
                  bg-color="white"
                  dense
                  :rules="[val => !!val || 'Kontak harus diisi']"
                >
                  <template v-slot:prepend>
                    <q-icon name="contact_phone" color="primary" />
                  </template>
                </q-input>

                <q-input 
                  v-model="pesan" 
                  outlined 
                  label="Deskripsi Masalah" 
                  type="textarea" 
                  bg-color="white"
                  :rules="[val => !!val || 'Deskripsi masalah harus diisi']"
                >
                  <template v-slot:prepend>
                    <q-icon name="report_problem" color="primary" class="q-mt-xs" />
                  </template>
                </q-input>

                <div>
                  <q-btn label="Kirim Laporan" type="submit" color="primary" unelevated class="full-width q-py-sm text-weight-bold" style="border-radius: 8px;" />
                  <q-btn label="Kembali ke Login" to="/login" flat color="grey-7" class="full-width q-mt-sm" no-caps />
                </div>

              </q-form>
            </q-card-section>
          </q-card>
        </div>

      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const router = useRouter()

const nama = ref('')
const kontak = ref('')
const pesan = ref('')

const kirimLaporan = () => {
  $q.loading.show({ message: 'Mengirim laporan...' })
  
  setTimeout(() => {
    $q.loading.hide()
    $q.notify({
      type: 'positive',
      icon: 'check_circle',
      message: 'Laporan berhasil dikirim! Admin akan menghubungi Anda.'
    })
    router.push('/login')
  }, 1500)
}
</script>

<style scoped>
.text-primary { color: #006837 !important; }
.bg-primary { background-color: #006837 !important; }
</style>