from app.models.payment.payment_strategy import PaymentStrategy

class GooglePayStrategy(PaymentStrategy):
    def process(self):
        self.is_ready_to_pay()
        self.create_transaction()
        print("Processing payment with Google Pay")


    
    def is_ready_to_pay(self):
        pass

    def create_transaction(self):
        pass

