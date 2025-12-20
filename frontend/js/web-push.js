/**
 * @file: web-push.js
 * @description: Quản lý Service Worker và Web Push Notifications.
 */

const publicVapidKey = "BPYjU2RmpapFkN9fum8yL92bSB_4ECeGfCN0ZizESu6kCusWocj2Qh-xbXaAMgE0Fdyr9--gqTS2B7MYXDspXp4";


/**
 * Đăng ký Service Worker
 * @returns {Promise<ServiceWorkerRegistration|null>}
 */
export async function registerServiceWorker() {
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    return await navigator.serviceWorker.register('/service-worker.js');
  }
  return null;
}


/**
 * Yêu cầu quyền thông báo từ trình duyệt
 * @returns {Promise<boolean>} - True nếu được cấp quyền
 */
export async function askNotificationPermission() {
  const permission = await Notification.requestPermission();
  return permission === "granted";
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');
  const rawData = atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}


/**
 * Đăng ký Push Subscription cho user hiện tại
 * @returns {Promise<PushSubscription>}
 */
export async function subscribeUserToPush() {
  const sw = await registerServiceWorker();
  if (!sw) return;

  let subscription = await sw.pushManager.getSubscription();
  if (!subscription) {
    subscription = await sw.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(publicVapidKey)
    });
  }

  localStorage.setItem("push_subscription", JSON.stringify({
    endpoint: subscription.endpoint,
    p256dh: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('p256dh')))),
    auth: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('auth'))))
  }));

  return subscription;
}


/**
 * Gửi thông tin subscription lên server để lưu db
 * @param {PushSubscription} subscription
 */
export async function sendSubscriptionToServer(subscription) {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");

  const payload = {
    endpoint: subscription.endpoint,
    p256dh: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('p256dh')))),
    auth: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('auth'))))
  };

  await fetch("http://localhost:8000/api/notifications/subscribe", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `${token_type} ${token}`
    },
    body: JSON.stringify(payload)
  });
}


/**
 * Hủy đăng ký Push Notification (unsubscribe)
 */
export async function unsubscribePush() {
  const token = localStorage.getItem("access_token");
  const token_type = localStorage.getItem("token_type");

  let subscription = null;
  const sw = await navigator.serviceWorker.ready;
  try {
    subscription = await sw.pushManager.getSubscription();
  } catch (err) {
    console.warn("PushManager.getSubscription() failed", err);
  }

  let payload;
  if (subscription) {
    payload = {
      endpoint: subscription.endpoint,
      p256dh: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('p256dh')))),
      auth: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('auth'))))
    };
  } else {
    const saved = localStorage.getItem("push_subscription");
    if (!saved) return;
    payload = JSON.parse(saved);
  }

  await fetch("http://localhost:8000/api/notifications/unsubscribe", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `${token_type} ${token}`
    },
    body: JSON.stringify(payload)
  });

  if (subscription) await subscription.unsubscribe();
  localStorage.removeItem("push_subscription");
}


/**
 * Khởi tạo toàn bộ quy trình Push Notification
 */
export async function initPush() {
  if (Notification.permission === "denied") {
    await unsubscribePush();
    return;
  }

  const granted = await askNotificationPermission();
  if (!granted) return;

  const subscription = await subscribeUserToPush();
  if (subscription) await sendSubscriptionToServer(subscription);
}
