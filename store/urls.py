from django.urls import path
from .import views
urlpatterns = [
    
    path('', views.home,name='home'),
    path('category/<int:id>/',views.category_products,name='category_products'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:id>/', views.increase_qty, name='increase_qty'),
    path('cart/decrease/<int:id>/', views.decrease_qty, name='decrease_qty'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
]