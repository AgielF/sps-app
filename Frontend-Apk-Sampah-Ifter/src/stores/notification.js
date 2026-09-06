import { api } from 'boot/axios'

const state = {
  notifications: [],
  unreadCount: 0,
  connectionStatus: 'disconnected',
  onlineStats: null,
}

const mutations = {
  SET_NOTIFICATIONS(state, notifications) {
    state.notifications = notifications
  },

  ADD_NOTIFICATION(state, notification) {
    // Avoid duplicates
    const exists = state.notifications.some((n) => n.id === notification.id)
    if (!exists) {
      state.notifications.unshift(notification)
    }
  },

  MARK_AS_READ(state, notificationId) {
    const index = state.notifications.findIndex((n) => n.id === notificationId)
    if (index !== -1) {
      state.notifications[index].read = true
    }
  },

  MARK_ALL_READ(state) {
    state.notifications.forEach((n) => {
      n.read = true
    })
  },

  CLEAR_NOTIFICATIONS(state) {
    state.notifications = []
  },

  SET_UNREAD_COUNT(state, count) {
    state.unreadCount = count
  },

  SET_CONNECTION_STATUS(state, status) {
    state.connectionStatus = status
  },

  SET_ONLINE_STATS(state, stats) {
    state.onlineStats = stats
  },
}

const actions = {
  async loadNotifications({ commit, rootState }) {
    try {
      const userId = rootState.auth.user?.id
      if (!userId) return

      const response = await api.get(`/notifications/history?user_id=${userId}`)
      if (response.data.success) {
        commit('SET_NOTIFICATIONS', response.data.notifications)
      }
    } catch (error) {
      console.error('Failed to load notifications:', error)
    }
  },

  async markAsRead({ commit }, notificationId) {
    try {
      commit('MARK_AS_READ', notificationId)
      // You might want to send to server here
    } catch (error) {
      console.error('Failed to mark as read:', error)
    }
  },

  async markAllAsRead({ commit }) {
    commit('MARK_ALL_READ')
    // You might want to send to server here
  },

  async clearNotifications({ commit }) {
    commit('CLEAR_NOTIFICATIONS')
  },
}

const getters = {
  unreadNotifications: (state) => {
    return state.notifications.filter((n) => !n.read)
  },

  jadwalNotifications: (state) => {
    return state.notifications.filter((n) => n.type === 'jadwal')
  },

  notificationCounts: (state) => {
    return {
      total: state.notifications.length,
      unread: state.notifications.filter((n) => !n.read).length,
      jadwal: state.notifications.filter((n) => n.type === 'jadwal').length,
    }
  },
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
}
