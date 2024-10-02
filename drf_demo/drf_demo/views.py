from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .serializers import OTPRequestSerializer, CustomTokenObtainPairSerializer
import random
import string


User = get_user_model()


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


class OTPRequestView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )

            otp = generate_otp()

            # 將 OTP 存儲在 Redis 中，設置 5 分鐘過期
            cache.set(f"otp_{username}", otp, timeout=300)

            # 發送 OTP 郵件
            send_mail(
                "Your OTP for Authentication",
                f"Your OTP is: {otp}. It will expire in 5 minutes.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "OTP sent successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        access_token = serializer.validated_data["access"]
        refresh_token = serializer.validated_data["refresh"]

        response = Response(
            {"access": access_token, "message": "Authentication successful"},
            status=status.HTTP_200_OK,
        )

        try:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                samesite="None",  # 對於跨域請求，使用 'None'
                secure=False,  # 在生產環境應該設為 True
                domain=None,  # 如果需要，指定域名
                max_age=3600 * 24 * 14,  # 14 days
            )
        except Exception as e:
            print(f"Error: {str(e)}")
        return response


class CustomTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        print(f"Refresh token: {refresh_token}")
        if not refresh_token:
            return Response(
                {"error": "No refresh token provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            response = Response(
                {"access": access_token, "message": "Token refreshed successfully"}
            )

            # 可選：更新 refresh token
            new_refresh_token = str(token)
            response.set_cookie(
                "refresh_token",
                new_refresh_token,
                httponly=True,
                samesite="Lax",
                path="/",
                max_age=3600 * 24 * 14,  # 14 days
            )

            return response

        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


from rest_framework.permissions import IsAuthenticated
from .custom_authentication import CustomJWTAuthentication


class ProtectedView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        return Response(
            {
                "message": "You have accessed a protected view!",
                "user": (
                    request.user.username
                    if request.user.is_authenticated
                    else "Anonymous"
                ),
            }
        )


class DebugView(APIView):
    authentication_classes = []  # 禁用身份驗證
    permission_classes = []  # 禁用權限檢查

    def get(self, request):
        return Response(
            {
                "headers": dict(request.headers),
                "cookies": request.COOKIES,
                "method": request.method,
                "content_type": request.content_type,
            }
        )
