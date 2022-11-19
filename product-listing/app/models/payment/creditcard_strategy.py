from app.models.payment.payment_strategy import PaymentStrategy


class CreditCardStrategy(PaymentStrategy):
    def process(self):
        print("Processing payment with CreditCard")
