from app.models.payment.payment_strategy import PaymentStrategy

class CrediCardStrategy(PaymentStrategy):
    def process(self):
        print("Processing payment with CreditCard")