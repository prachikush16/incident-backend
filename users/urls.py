from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import (
    RegisterView, ProfileView, PincodeLookupView,
    ChangePasswordView, SendOTPView, VerifyOTPView, ResetPasswordWithOTPView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('pincode/<str:pincode>/', PincodeLookupView.as_view(), name='pincode-lookup'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('forgot-password/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('forgot-password/reset/', ResetPasswordWithOTPView.as_view(), name='reset-password-otp'),
]
