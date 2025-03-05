from mongoengine import Document, StringField, DecimalField, IntField, BooleanField

class Product(Document):
    name = StringField(max_length=255, required=True)
    price = DecimalField(min_value=0, precision=2, required=True)
    stock = IntField(default=0, required=True)
    description = StringField()
    image_base64 = StringField()

    meta = {'allow_inheritance': True, 'collection': 'products'}

# Book Model
class Book(Product):
    author = StringField(max_length=255, required=True)
    isbn = StringField(max_length=20, required=True)
    publisher = StringField(max_length=255)

# Clothes Model
class Clothes(Product):
    size = StringField(max_length=10, required=True)  
    color = StringField(max_length=50, required=True)
    material = StringField(max_length=100, required=True)

# Mobile Model
class Mobile(Product):
    brand = StringField(max_length=255, required=True)
    ram = IntField(required=True) 
    storage = IntField(required=True)  
    is_5g_supported = BooleanField(default=False)
