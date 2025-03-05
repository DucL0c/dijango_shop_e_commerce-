from django.urls import path
from .views import ProcessPaymentView, PaymentDetailView, PaymentListView

urlpatterns = [
    path('process/', ProcessPaymentView.as_view(), name='process-payment'),
    path('<int:payment_id>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('', PaymentListView.as_view(), name='payment-list'),
]