from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
    UserListAPIView,
    UserLoginAPIView,
    UserRetrieveUpdateDestroyAPIView,
    RegisterAPIView,
    PasswordResetAPIView,
    LogoutAPIView,
    LogoutAllDevicesAPIView
)


urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_update_destroy'),
    path('password_reset/', PasswordResetAPIView.as_view(), name='password_reset_api'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('logout_all/', LogoutAllDevicesAPIView.as_view(), name='logout_all_devices'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]