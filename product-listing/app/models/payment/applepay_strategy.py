from app.models.payment.payment_strategy import PaymentStrategy


class ApplePayStrategy(PaymentStrategy):
    def process(self):
        print("Processing payment with Apple Pay")
