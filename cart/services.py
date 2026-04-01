from django.db import transaction

from cart.models import Cart, CartItem


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()

        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


@transaction.atomic
def add_product_to_cart(cart, product, quantity=1):
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},
    )
    new_quantity = quantity if created else item.quantity + quantity

    if new_quantity > product.stock:
        raise ValueError("Not enough stock.")

    item.quantity = new_quantity
    item.save()
    return item


@transaction.atomic
def update_cart_item_quantity(item, quantity):
    if quantity > item.product.stock:
        raise ValueError("Not enough stock.")

    if quantity <= 0:
        item.delete()
        return None

    item.quantity = quantity
    item.save(update_fields=["quantity"])
    return item


@transaction.atomic
def clear_cart(cart):
    cart.items.all().delete()


@transaction.atomic
def merge_session_cart_to_user(request):
    if not request.user.is_authenticated or not request.session.session_key:
        return

    session_cart = Cart.objects.filter(session_key=request.session.session_key).first()
    if not session_cart:
        return

    user_cart, _ = Cart.objects.get_or_create(user=request.user)

    if session_cart.id == user_cart.id:
        return

    for session_item in session_cart.items.select_related("product"):
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=session_item.product,
            defaults={"quantity": session_item.quantity},
        )
        if not created:
            user_item.quantity += session_item.quantity
            user_item.save(update_fields=["quantity"])

    session_cart.delete()
