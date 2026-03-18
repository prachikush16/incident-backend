import requests
from django.conf import settings as django_settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import User, PasswordResetOTP
from users.serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PincodeLookupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pincode):
        try:
            url = f"{django_settings.PINCODE_API_URL}/{pincode}"
            timeout = django_settings.PINCODE_API_TIMEOUT
            resp = requests.get(url, timeout=timeout)
            data = resp.json()
            if data and data[0]['Status'] == 'Success':
                post_office = data[0]['PostOffice'][0]
                return Response({
                    'city': post_office.get('District', ''),
                    'state': post_office.get('State', ''),
                    'country': post_office.get('Country', ''),
                })
        except Exception:
            pass
        return Response({'error': 'Invalid or unknown pincode'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully'})


# ── OTP-based Forgot Password ─────────────────────────────────────────────────

class SendOTPView(APIView):
    """Step 1: User submits email → generate & print OTP (console backend)."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.generate_for(user)
            # In production replace with SMS/email gateway; console output for now
            print(f"\n[OTP] Password reset OTP for {email}: {otp_obj.otp}\n")
        except User.DoesNotExist:
            pass  # Don't reveal whether email exists
        return Response({'message': 'If the email is registered, an OTP has been sent.'})


class VerifyOTPView(APIView):
    """Step 2: Verify the OTP is correct and not expired."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        otp = request.data.get('otp', '').strip()
        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp, is_used=False).last()
            if not otp_obj or not otp_obj.is_valid():
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'OTP verified.'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordWithOTPView(APIView):
    """Step 3: Submit email + OTP + new password to complete reset."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        otp = request.data.get('otp', '').strip()
        new_password = request.data.get('new_password', '')

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp, is_used=False).last()
            if not otp_obj or not otp_obj.is_valid():
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return Response({'error': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            otp_obj.is_used = True
            otp_obj.save()
            return Response({'message': 'Password reset successful.'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
