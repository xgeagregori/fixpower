from enum import Enum

from app.models.payment.applepay_strategy import ApplePayStrategy
from app.models.payment.creditcard_strategy import CreditCardStrategy
from app.models.payment.googlepay_strategy import GooglePayStrategy
from app.models.payment.paypal_strategy import PaypalStrategy
from app.services.payment_service import PaymentService, PaymentStrategyFactory


class PaymentMethod(str, Enum):
    APPLE_PAY = "APPLE_PAY"
    CREDIT_CARD = "CREDIT_CARD"
    GOOGLE_PAY = "GOOGLE_PAY"
    PAYPAL = "PAYPAL"


class PaymentServiceImpl(PaymentService):
    def create_payment_strategy(self, payment_method: PaymentMethod):
        if payment_method == PaymentMethod.APPLE_PAY:
            payment_strategy = ApplePayStrategyFactory().create_payment_strategy()
        elif payment_method == PaymentMethod.CREDIT_CARD:
            payment_strategy = CreditCardStrategyFactory().create_payment_strategy()
        elif payment_method == PaymentMethod.GOOGLE_PAY:
            payment_strategy = GooglePayStrategyFactory().create_payment_strategy()
        elif payment_method == PaymentMethod.PAYPAL:
            payment_strategy = PaypalStrategyFactory().create_payment_strategy()

        return payment_strategy


class ApplePayStrategyFactory(PaymentStrategyFactory):
    def create_payment_strategy(self):
        return ApplePayStrategy()


class CreditCardStrategyFactory(PaymentStrategyFactory):
    def create_payment_strategy(self):
        return CreditCardStrategy()


class GooglePayStrategyFactory(PaymentStrategyFactory):
    def create_payment_strategy(self):
        return GooglePayStrategy()


class PaypalStrategyFactory(PaymentStrategyFactory):
    def create_payment_strategy(self):
        return PaypalStrategy()
