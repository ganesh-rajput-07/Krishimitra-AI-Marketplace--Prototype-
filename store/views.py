from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Import User model for dummy users
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Product, Cart, Order
from .forms import ProductForm

# Get or create a dummy user for testing
def get_dummy_user():
    user, _ = User.objects.get_or_create(username="dummy_farmer", defaults={"email": "dummy@example.com"})
    return user

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

from django.http import JsonResponse
import json

def remove_from_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = str(data.get('product_id'))  # Ensure ID is a string
            cart = request.session.get('cart', {})

            if product_id in cart:
                del cart[product_id]  # Remove the item
                request.session['cart'] = cart  # Save back to session
                request.session.modified = True  # Ensure session updates

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=400)

from django.shortcuts import render, redirect
from .models import Order, Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Product
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        # Validate product_id and quantity
        if not product_id or not quantity:
            return render(request, "checkout.html", {"error": "Invalid product or quantity"})

        try:
            quantity = int(quantity)
            product = get_object_or_404(Product, id=product_id)
            total_price = product.price * quantity

            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                total_price=total_price
            )

            return redirect("order_success")  # Redirect to a success page

        except ValueError:
            return render(request, "store/checkout.html", {"error": "Invalid quantity value"})

    return render(request, "store/checkout.html")

def payment_success(request):
    messages.success(request, "Payment successful! Your order has been placed.")
    return redirect('home')

def add_product(request):
    user = request.user if request.user.is_authenticated else get_dummy_user()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = user  # Assign the dummy farmer if no auth
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()  # Ensure this fetches products correctly
    return render(request, 'store/product_list.html', {'products': products})

def farmer_dashboard(request):
    user = request.user if request.user.is_authenticated else get_dummy_user()

    # Get all products added by the logged-in farmer
    farmer_products = Product.objects.filter(farmer=user)

    # Get sales data based on orders
    sales_data = (
        Order.objects.filter(products__in=farmer_products)  # Fetch orders that contain farmer's products
        .values('products__name')  # Get product names
        .annotate(total_sold=Sum('products__price'))  # Sum of prices (adjust as needed)
    )

    # Calculate total earnings from orders
    total_earnings = (
        Order.objects.filter(products__in=farmer_products)
        .aggregate(total=Sum('total_amount'))['total'] or 0
    )

    context = {
        'farmer_products': farmer_products,
        'sales_data': sales_data,
        'total_earnings': total_earnings,
    }
    return render(request, 'store/dashboard.html', context)

def selling_report(request):
    return render(request, 'store/selling_report.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, Order
from .forms import ProductForm

# ✅ User Registration View
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Choose another.")
            return redirect("register")

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("register")

        # Create and log in user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'authentication/register.html')

# ✅ User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'authentication/login.html')

# ✅ User Logout View
def user_logout(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

from django.shortcuts import render

def landing_page(request):
    return render(request, "landing.html")  # Ensure the template is in the correct folder
