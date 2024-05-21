from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django_otp.plugins.otp_totp.models import TOTPDevice
import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
from .models import TwoFactorAuth

class Enable2FA(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        key = pyotp.random_base32()
        
        TOTPDevice.objects.filter(user=user).delete()
        device = TOTPDevice.objects.create(user=user, name='default', key=key)
        totp = pyotp.TOTP(key)
        
        # Generate QR Code
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(totp.provisioning_uri(user.email, issuer_name="My App"), image_factory=factory)
        stream = BytesIO()
        img.save(stream)
        svg_qr = stream.getvalue().decode()
        
        # Generate backup codes
        backup_codes = [pyotp.random_base32() for _ in range(5)]
        
        # Save to database
        TwoFactorAuth.objects.update_or_create(
            user=user,
            defaults={'qr_code': svg_qr, 'backup_codes': backup_codes}
        )
        
        # Send email
        send_mail(
            'Your 2FA QR Code and Backup Codes',
            f'Your backup codes: {", ".join(backup_codes)}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            'svg_qr': svg_qr,
            'backup_codes': backup_codes
        }, status=status.HTTP_200_OK)

class Disable2FA(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        TOTPDevice.objects.filter(user=user).delete()
        TwoFactorAuth.objects.filter(user=user).delete()
        return Response(status=status.HTTP_200_OK)

class Verify2FACode(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        code = request.data.get('code')
        device = TOTPDevice.objects.filter(user=user, name='default').first()

        if device and device.verify_token(code):
            return Response(status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid 2FA code'}, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        code = request.data.get('code')
        
        user = authenticate(email=email, password=password)
        if user:
            device = TOTPDevice.objects.filter(user=user, name='default').first()
            if device:
                totp = pyotp.TOTP(device.key)
                
                if not code:
                    otp = totp.now()
                    cache.set(f"otp_{user.id}", otp, timeout=300)  # Store for 5 minutes

                    # Send email with OTP
                    send_mail(
                        'Your 2FA Code',
                        f'Your 2FA code is: {otp}',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False
                    )

                    return Response({'detail': '2FA code sent to your email'}, status=status.HTTP_401_UNAUTHORIZED)

                # Verify the code from email or authenticator app
                email_otp = cache.get(f"otp_{user.id}")
                if totp.verify(code, valid_window=1) or code == email_otp:
                    cache.delete(f"otp_{user.id}")
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                
                return Response({'detail': 'Invalid 2FA code'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # If no TOTPDevice is found, proceed with login without 2FA
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class Retrieve2FA(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            two_factor_auth = TwoFactorAuth.objects.get(user=user)
            return Response({
                'svg_qr': two_factor_auth.qr_code,
                'backup_codes': two_factor_auth.backup_codes
            }, status=status.HTTP_200_OK)
        except TwoFactorAuth.DoesNotExist:
            return Response({'detail': '2FA not enabled'}, status=status.HTTP_404_NOT_FOUND)