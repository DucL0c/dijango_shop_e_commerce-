import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer

PRODUCT_SERVICE_URL = "http://127.0.0.1:8000/api/product"
CUSTOMER_SERVICE_URL = "http://127.0.0.1:8000/api/user/profile"

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    # Get Cart Items
    def get(self, request):
        cart_items = Cart.objects.filter(user_id=request.user.id)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)
        # total_price = sum(item.price * item.quantity for item in cart_items)
        
        # return Response({
        #     "cart_items": serializer.data,
        #     "total_price": total_price
        # })

    # Add to Cart
    def post(self, request):
        product_id = request.data.get("product_id")
        product_type = request.data.get("product_type")

        # Fetch product details from Product Service
        product_url = f"{PRODUCT_SERVICE_URL}/{product_type}/{product_id}/"
        product_response = requests.get(product_url)

        if product_response.status_code != 200:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product_data = product_response.json()
        price = product_data["price"]

        cart_item, created = Cart.objects.get_or_create(
            user_id=request.user.id,
            product_id=product_id,
            product_type=product_type,
            defaults={"quantity": request.data.get("quantity", 1), "price": price}
        )

        if not created:
            cart_item.quantity += request.data.get("quantity", 1)
            cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    # Update Cart Item Quantity
    def put(self, request, cart_id):
        try:
            cart_item = Cart.objects.get(id=cart_id, user_id=request.user.id)
            cart_item.quantity = request.data.get('quantity', cart_item.quantity)
            cart_item.save()
            return Response({"message": "Cart updated successfully"})
        except Cart.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Remove an Item from Cart
    def delete(self, request, cart_id):
        try:
            cart_item = Cart.objects.get(id=cart_id, user_id=request.user.id)
            cart_item.delete()
            return Response({"message": "Item removed from cart"})
        except Cart.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

# Clear Entire Cart
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Cart.objects.filter(user_id=request.user.id).delete()
        return Response({"message": "Cart cleared successfully"})
