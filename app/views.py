from django.shortcuts import render, redirect
from django.views import View
from .models  import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

# Create your views here.
# Product View
class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        laptops = Product.objects.filter(category='L')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        
        return render(request, 'app/home.html', {
            'topwears': topwears,
            'laptops': laptops,
            'bottomwears': bottomwears,
            'mobiles': mobiles
        })
# Product Detail View 
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        
        item_already_in_cart = False
        if request.user.is_authenticated:
             if request.user.is_authenticated:
              item_already_in_cart = Cart.objects.filter(
            Q(product=product.id) & Q(user=request.user)
        ).exists()

        return render(request, 'app/productdetail.html', {
            'product': product,
            'item_already_in_cart': item_already_in_cart
        })

# Add to Cart
@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

# Show Cart
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user) 
        cart_item_count = cart.count() 
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        if cart.exists():  
            for p in cart:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
            totalamount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'amount': amount, 'totalamount': totalamount, 'cart_item_count': cart_item_count})
        else:
            return render(request, 'app/emptycart.html')
        
# Plus Cart
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']                            
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all()if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

# Minus Cart   
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']                            
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all()if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
    
# Remove Cart 
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']                            
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all()if p.user == request.user]
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
   
# Buy Now
def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    def post(self, request):
       form = CustomerProfileForm(request.POST)
       if form.is_valid():
        usr = request.user
        name = form.cleaned_data['name']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']
        reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)       
        reg.save()
        messages.success(request, 'Congratulations! Profile updated successfully.')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary','active': 'btn-primary'})    
@login_required
# Addresses
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add,'active': 'btn-primary'})
# Orders
@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed': op, 'active': 'btn-primary'})

@login_required
# Mobile
def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=50000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=50000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})

@login_required
# Laptop
def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')  # Assuming 'L' is the code for Laptop
    elif data == 'Dell' or data == 'HP':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    return render(request, 'app/laptop.html', {'laptops': laptops})

@login_required
# Top Wear
def top(request, data=None):
    if data == None:
        tops = Product.objects.filter(category='TW')
    elif data == 'below':
        tops = Product.objects.filter(category='TW').filter(discounted_price__lt=10000)
    elif data == 'above':
        tops = Product.objects.filter(category='TW').filter(discounted_price__gt=10000)
    elif data == 'Puma' or data == 'Nike':
        tops = Product.objects.filter(category='TW').filter(brand=data) 
    return render(request, 'app/top.html', {'tops': tops})

@login_required
# Bottom Wear
def bottom(request, data=None):
    if data == None:
        bottoms = Product.objects.filter(category='BW')
    elif data == 'below':
        bottoms = Product.objects.filter(category='BW').filter(discounted_price__lt=10000)
    elif data == 'above':
        bottoms = Product.objects.filter(category='BW').filter(discounted_price__gt=10000)
    elif data == 'Puma' or data == 'Nike':
        bottoms = Product.objects.filter(category='BW').filter(brand=data)
    return render(request, 'app/bottom.html', {'bottoms': bottoms})

# Login
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered successfully.')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

# Check out
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    
    for p in cart_items:
        tempamount = (p.quantity * (p.product.discounted_price or 0))
        amount += tempamount
    
    totalamount = amount + shipping_amount
    
    return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'totalamount': totalamount})


# Payment Done
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.filter(id=custid, user=user).first()
    if customer is None:
        return HttpResponse("Customer not found!", status=404)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')







# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

# def home(request):
#  return render(request, 'app/home.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

# def profile(request):
#  return render(request, 'app/profile.html')
