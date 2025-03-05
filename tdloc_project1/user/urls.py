from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, UserListView, UpdateUserRoleView, DeleteUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Admin APIs
    path('ad/', UserListView.as_view(), name='user_list'),
    path('ad/role/<int:user_id>/', UpdateUserRoleView.as_view(), name='update_role'),
    path('ad/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
]
