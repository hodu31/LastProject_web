self.addEventListener('install', function (event) {
  // 서비스 워커 설치시 실행할 작업
})

self.addEventListener('activate', function (event) {
  // 서비스 워커 활성화시 실행할 작업
})

self.addEventListener('push', function (event) {
  const payload = event.data ? event.data.text() : 'no payload'

  const options = {
    body: payload,
    icon: '/static/mainapp/dist/img/위험.png',
    vibrate: [100, 50, 100],
  }

  event.waitUntil(self.registration.showNotification('노티케어', options))
})
