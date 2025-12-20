import json
import os
from dotenv import load_dotenv
from pywebpush import webpush, WebPushException

load_dotenv()

VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")

def send_webpush_api(title: str, message: str, sub: dict):
    payload = json.dumps({
        "title": title,
        "body": message
    })

    try:
        webpush(
            subscription_info={
                "endpoint": sub["endpoint"],
                "keys": {
                    "p256dh": sub["p256dh"],
                    "auth": sub["auth"]
                }
            },
            data=payload,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={
                "sub": "mailto:admin@volunteerhub.com"
            }
        )
    except WebPushException as e:
        print(f"Lỗi gửi tới {sub['endpoint']}: {e}")


def send_webpush(title: str, message: str, subscriptions: list):
    for sub in subscriptions:
        send_webpush_api(title, message, sub)