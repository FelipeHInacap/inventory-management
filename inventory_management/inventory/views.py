

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .factories import ProductFactory

from .models import Product, Sale, Notification
from django.core.mail import send_mail
from .forms import ProductForm, SaleForm 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Registrar venta
def register_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            product = sale.product
            if product.stock >= sale.quantity:
                product.stock -= sale.quantity
                product.save()
                sale.save()
                if product.stock <= product.stock_alert_threshold:
                    Notification.objects.create(
                        product=product,
                        message=f"El producto '{product.name}' está por agotarse. Cantidad actual: {product.stock}."
                    )
                return redirect('product_list')
            else:
                return render(request, 'inventory/sale_form.html', {
                    'form': form,
                    'error': 'Stock insuficiente'
                })
    else:
        form = SaleForm()
    return render(request, 'inventory/sale_form.html', {'form': form})


def send_stock_alerts():
    notifications = Notification.objects.filter(product__stock__lte=10)
    for notification in notifications:
        send_mail(
            'Alerta de Stock',
            notification.message,
            'no-reply@example.com',
            [notification.product.manager.email] 
        )


# Crear producto
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Usar la fábrica para crear el producto
            ProductFactory.create_product(
                name=data['name'],
                description=data.get('description', ''),
                stock=data['stock'],
                stock_alert_threshold=data['stock_alert_threshold'],
                barcode=data['barcode']
            )
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

# Listar productos
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'inventory/login.html')


@login_required
def home(request):
    return render(request, 'inventory/home.html') 


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if not User.objects.filter(username=username).exists():  # Verifica si el usuario ya existe
                User.objects.create_user(username=username, password=password)
                messages.success(request, "Usuario creado exitosamente. ¡Inicia sesión!")
                return redirect('login')  # Redirige al login
            else:
                messages.error(request, "El nombre de usuario ya existe.")
        else:
            messages.error(request, "Las contraseñas no coinciden.")

    return render(request, 'inventory/registrarse.html')


from django.shortcuts import render
from .models import Product
from django.db.models import F

def home(request):
    # Filtrar productos cuyo stock esté en o por debajo del umbral de alerta
    low_stock_products = Product.objects.filter(stock__lte=F('stock_alert_threshold'))

    # Renderizar la página con los productos filtrados
    return render(request, 'inventory/home.html', {'low_stock_products': low_stock_products})
