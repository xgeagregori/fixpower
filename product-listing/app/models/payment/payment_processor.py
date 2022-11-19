from app.models.payment.payment_strategy import PaymentStrategy

class PaymentProcessor:
    def __init__(self, strategy:PaymentStrategy):
        self.strategy = strategy
    
    def process(self):
        self.strategy.process()
    
    def cancel(self):
        pass
