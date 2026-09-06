<template>
  <q-layout view="hHh LpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <!-- Logo/Brand -->
        <q-toolbar-title>
          <q-avatar>
            <img src="logo.png" alt="Logo" />
          </q-avatar>
          SPS App
        </q-toolbar-title>

        <!-- Spacer -->
        <q-space />

        <!-- Notifications -->
        <notification-system :user="user" class="q-mr-sm" v-if="user" />

        <!-- User Menu -->
        <q-btn flat round dense icon="person">
          <q-menu>
            <q-list style="min-width: 150px">
              <q-item clickable v-close-popup>
                <q-item-section avatar>
                  <q-icon name="person" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ user?.nama || user?.username }}</q-item-label>
                  <q-item-label caption>{{ user?.role }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup @click="logout">
                <q-item-section avatar>
                  <q-icon name="logout" />
                </q-item-section>
                <q-item-section>Logout</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <!-- Page Content -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import NotificationSystem from 'components/NotificationSystem.vue'

export default defineComponent({
  name: 'MainLayout',
  components: {
    NotificationSystem,
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const user = computed(() => store.state.auth.user)

    const logout = async () => {
      await store.dispatch('auth/logout')
      router.push('/login')
    }

    return {
      user,
      logout,
    }
  },
})
</script>
