from django.urls import path
from .views import home, add_to_cart, view_cart, remove_from_cart, checkout, payment_success, add_product, product_list, farmer_dashboard, selling_report, user_login, user_register, user_logout, product_detail, landing_page

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path('/home/', home, name='home'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment-success/', payment_success, name='payment_success'),

    path('products/', product_list, name='product_list'),
    path('add-product/', add_product, name='add_product'),
    path('farmer/dashboard/', farmer_dashboard, name='farmer_dashboard'),
    path('farmer/selling-report/', selling_report, name='selling_report'),
]
