from django.urls import path
from .views import CartView, ClearCartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<int:cart_id>/', CartView.as_view(), name='update_cart'),
    path('clear/', ClearCartView.as_view(), name='clear_cart'),
]
