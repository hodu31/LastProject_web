self.addEventListener('install', function (event) {
  console.log('Service Worker Installed')
})

self.addEventListener('activate', function (event) {
  console.log('Service Worker Activated')
})

// 수정된 코드
self.addEventListener('message', function (event) {
  if (event.data && event.data.type === 'detect-push') {
    self.registration.showNotification('노티케어', {
      body: event.data.message,
      icon: event.data.icon,
    })
  }
})

// 기존 코드 유지
self.addEventListener('notificationclick', function (event) {
  event.notification.close()
})
