import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Shipment
from .serializers import ShipmentSerializer

ORDER_SERVICE_URL = "http://127.0.0.1:8000/api/order/"

class CreateShipmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        user_id = request.data.get('user_id')
        address = request.data.get('address')

        if not all([order_id, user_id, address]):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        shipment = Shipment.objects.create(order_id=order_id, user_id=user_id, address=address)
        shipment.tracking_number = f"TRK_{shipment.id}"
        shipment.status = 'shipped'
        shipment.save()

        # Update Order Status
        order_update_response = requests.put(
            f"{ORDER_SERVICE_URL}{order_id}/",
            headers={"Authorization": f"Bearer {request.auth}"},
            json={"status": "shipped"}
        )

        # Log the response information
        print("Order Update Response Status Code:", order_update_response.status_code)
        print("Order Update Response Content:", order_update_response.content)

        if order_update_response.status_code != 200:
            return Response({"error": "Failed to update order status"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED)

class ShipmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, shipment_id):
        try:
            shipment = Shipment.objects.get(id=shipment_id, user_id=request.user.id)
            return Response(ShipmentSerializer(shipment).data)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, shipment_id):
        try:
            shipment = Shipment.objects.get(id=shipment_id, user_id=request.user.id)
            shipment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

class ShipmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shipments = Shipment.objects.filter(user_id=request.user.id)
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)