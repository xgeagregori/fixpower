from app.models.payment.payment_strategy import PaymentStrategy


class GooglePayStrategy(PaymentStrategy):
    def process(self):
        print("Processing payment with Google Pay")
