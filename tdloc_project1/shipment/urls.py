from django.urls import path
from .views import CreateShipmentView, ShipmentDetailView, ShipmentListView

urlpatterns = [
    path('create/', CreateShipmentView.as_view(), name='create-shipment'),
    path('<int:shipment_id>/', ShipmentDetailView.as_view(), name='shipment-detail'),
    path('', ShipmentListView.as_view(), name='shipment-list'),
]