self.addEventListener('push', function (event) {
  var options = {
    body: event.data.text(),
  }

  event.waitUntil(
    self.registration.showNotification('Push Notification', options)
  )
})
