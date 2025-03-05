from rest_framework import serializers
from .models import Book, Clothes, Mobile

class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    description = serializers.CharField()
    image_base64 = serializers.CharField()
    author = serializers.CharField(max_length=255)
    isbn = serializers.CharField(max_length=20)
    publisher = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance.reload()

class ClothesSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    description = serializers.CharField()
    image_base64 = serializers.CharField()
    size = serializers.CharField(max_length=10)
    color = serializers.CharField(max_length=50)
    material = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Clothes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance.reload()

class MobileSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    description = serializers.CharField()
    image_base64 = serializers.CharField()
    brand = serializers.CharField(max_length=255)
    ram = serializers.IntegerField()
    storage = serializers.IntegerField()
    is_5g_supported = serializers.BooleanField()

    def create(self, validated_data):
        return Mobile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance.reload()
