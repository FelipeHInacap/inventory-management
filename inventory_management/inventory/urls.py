from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),  # Ruta para la lista de productos
    path('home/', views.home, name='home'), 
    path('', views.login_view, name='login'),
    path('products/create/', views.product_create, name='product_create'),  # Ruta para crear un producto
    path('sales/register/', views.register_sale, name='register_sale'),  # Ruta para registrar una venta
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout')
]

