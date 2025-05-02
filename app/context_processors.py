# store/context_processors.py
from .models import Cart

def cart_item_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()  # Count items in the cart
    return {'cart_item_count': cart_count}
