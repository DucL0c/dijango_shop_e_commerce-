from django.urls import path
from .views import (
    BookListCreateView, BookDetailView,
    ClothesListCreateView,
    ClothesDetailView,
    MobileListCreateView,
    MobileDetailView
)

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<str:obj_id>/', BookDetailView.as_view(), name='book-detail'),
    
    path('clothes/', ClothesListCreateView.as_view(), name='clothes-list-create'),
    path('clothes/<str:obj_id>/', ClothesDetailView.as_view(), name='clothes-detail'),
    
    path('mobiles/', MobileListCreateView.as_view(), name='mobile-list-create'),
    path('mobiles/<str:obj_id>/', MobileDetailView.as_view(), name='mobile-detail'),
]
