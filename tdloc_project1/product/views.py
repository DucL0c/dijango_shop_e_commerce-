from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Clothes, Mobile
from .serializers import BookSerializer, ClothesSerializer, MobileSerializer
from bson import ObjectId

# Base class for common CRUD operations
class BaseListCreateView(APIView):
    model = None
    serializer_class = None

    def get(self, request):
        items = self.model.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseDetailView(APIView):
    model = None
    serializer_class = None

    def get(self, request, obj_id):
        try:
            obj = self.model.objects.get(id=ObjectId(obj_id))
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, obj_id):
        try:
            obj = self.model.objects.get(id=ObjectId(obj_id))
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, obj_id):
        try:
            obj = self.model.objects.get(id=ObjectId(obj_id))
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Book API
class BookListCreateView(BaseListCreateView):
    model = Book
    serializer_class = BookSerializer

class BookDetailView(BaseDetailView):
    model = Book
    serializer_class = BookSerializer

# Clothes API
class ClothesListCreateView(BaseListCreateView):
    model = Clothes
    serializer_class = ClothesSerializer

class ClothesDetailView(BaseDetailView):
    model = Clothes
    serializer_class = ClothesSerializer

# Mobile API
class MobileListCreateView(BaseListCreateView):
    model = Mobile
    serializer_class = MobileSerializer

class MobileDetailView(BaseDetailView):
    model = Mobile
    serializer_class = MobileSerializer
