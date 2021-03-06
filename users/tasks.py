from celery import shared_task
from project_bitlab.celery import app

@app.task(
    name='send_sms',
    bind=True,
    default_retry_delay=5,
    max_retries=1,
    acks_late=True
)
def send_sms(self, phone, otp):
    phone_num = str(phone)
    print("SMS SENT", phone, otp)
