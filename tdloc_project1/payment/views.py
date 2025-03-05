import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer

ORDER_SERVICE_URL = "http://127.0.0.1:8000/api/order/"

class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        user_id = request.data.get('user_id')
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')

        if not all([order_id, user_id, amount, payment_method]):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Payment Record
        payment = Payment.objects.create(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            payment_method=payment_method
        )

        # Simulate External Payment Gateway
        payment.transaction_id = f"TXN_{payment.id}"
        payment.status = 'completed'
        payment.save()

        # Update Order Status
        order_update_response = requests.put(
            f"{ORDER_SERVICE_URL}{order_id}/",
            headers={"Authorization": f"Bearer {request.auth}"},
            json={"status": "confirmed"}
        )

        # Log the response information
        print("Order Update Response Status Code:", order_update_response.status_code)
        print("Order Update Response Content:", order_update_response.content)

        if order_update_response.status_code != 200:
            return Response({"error": "Failed to update order status"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user_id=request.user.id)
            return Response(PaymentSerializer(payment).data)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user_id=request.user.id)
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user_id=request.user.id)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)