import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    """Создает продукт в Stripe."""
    try:
        product = stripe.Product.create(
            name=name,
            type="service",
        )
        return product.id
    except Exception as e:
        raise Exception(f"Ошибка при создании продукта в Stripe: {e}")


def create_stripe_price(product_id, amount, currency='rub'):
    """Создает цену в Stripe."""
    try:
        price = stripe.Price.create(
            unit_amount=int(amount * 100),  # Цена в копейках! Умножаем на 100 и преобразуем в int
            currency=currency,
            product=product_id,
        )
        return price.id
    except Exception as e:
        raise Exception(f"Ошибка при создании цены в Stripe: {e}")


def create_stripe_session(price_id, success_url, cancel_url):
    """Создает платежную сессию в Stripe."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.id, session.url  # Вернем ID сессии и URL
    except Exception as e:
        raise Exception(f"Ошибка при создании сессии в Stripe: {e}")
