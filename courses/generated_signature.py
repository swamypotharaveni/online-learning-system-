import hmac
import hashlib
from online_learning import settings
secret = settings.RAZORPAY_SECRET
order_id="order_Qv25y36n2TTbZC"
generated_signature = hmac.new(
        key=bytes(secret, 'utf-8'),
        msg=bytes(f"{order_id}|{payment_id}", 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()