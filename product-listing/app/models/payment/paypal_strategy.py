from app.models.payment.payment_strategy import PaymentStrategy


class PaypalStrategy(PaymentStrategy):
    def process(self):
        print("Processing payment with Paypal")
