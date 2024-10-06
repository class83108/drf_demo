from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.cache import cache

User = get_user_model()


class OTPRequestSerializer(serializers.Serializer):
    username = serializers.CharField(
        help_text="User's username",
        max_length=150,
        min_length=3,
    )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "username"
    otp = serializers.CharField(max_length=6, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"] = serializers.CharField(required=False, write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        username = attrs.get("username")
        otp = attrs.get("otp")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username")

        # 驗證 OTP
        stored_otp = cache.get(f"otp_{username}")
        if not stored_otp or stored_otp != otp:
            raise serializers.ValidationError("Invalid or expired OTP")

        # OTP 驗證成功，刪除存儲的 OTP
        cache.delete(f"otp_{username}")

        refresh = self.get_token(user)
        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
