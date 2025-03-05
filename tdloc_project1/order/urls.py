from django.urls import path
from .views import CreateOrderView, OrderDetailView, OrderListView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('', OrderListView.as_view(), name='order-list'),
]