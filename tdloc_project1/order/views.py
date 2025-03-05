import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer

CART_SERVICE_URL = "http://127.0.0.1:8000/api/cart/"

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id

        # Fetch cart items from Cart Service
        cart_response = requests.get(f"{CART_SERVICE_URL}", headers={"Authorization": f"Bearer {request.auth}"})
        if cart_response.status_code != 200:
            return Response({"error": "Failed to fetch cart"}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = cart_response.json()
        if not cart_items:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price
        total_price = sum(float(item["price"]) * int(item["quantity"]) for item in cart_items)

        # Create Order
        order = Order.objects.create(user_id=user_id, total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                product_type=item["product_type"],
                quantity=int(item["quantity"]),
                price=float(item["price"])
            )

        # Clear Cart after order
        requests.delete(f"{CART_SERVICE_URL}clear/", headers={"Authorization": f"Bearer {request.auth}"})

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user_id=request.user.id)
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user_id=request.user.id)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user_id=request.user.id)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user_id=request.user.id)
            status = request.data.get('status')
            if status and status in dict(Order.STATUS_CHOICES):
                order.status = status
                order.save()
                return Response(OrderSerializer(order).data)
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)