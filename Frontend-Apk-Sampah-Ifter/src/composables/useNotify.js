import { useQuasar } from 'quasar'

export function useNotify() {
  const $q = useQuasar()

  const notifySuccess = (message, position = 'top') => {
    $q.notify({
      type: 'positive',
      message,
      position,
      timeout: 2000,
      icon: 'check_circle'
    })
  }

  const notifyError = (message, position = 'top') => {
    $q.notify({
      type: 'negative',
      message,
      position,
      timeout: 3000,
      icon: 'warning'
    })
  }
  
  const notifyInfo = (message, position = 'top') => {
    $q.notify({
      type: 'info',
      message,
      position,
      timeout: 2000,
      icon: 'info'
    })
  }

  return {
    notifySuccess,
    notifyError,
    notifyInfo
  }
}
