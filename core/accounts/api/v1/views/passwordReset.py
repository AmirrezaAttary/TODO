from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from mail_templated import EmailMessage
from ...utils import EmailThread
from ....models import PasswordResetToken
from ..serializers import PasswordResetRequestSerializer
from django.utils import timezone

User = get_user_model()


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        raw_token, token_obj = PasswordResetToken.create_token(user)

        reset_link = f"http://127.0.0.1:8080/accounts/api/v1/reset-password/?token={raw_token}"

        email_obj = EmailMessage(
            'email/password_reset.tpl',
            {'reset_link': reset_link},
            'admin@admin.com',
            to=[email]
        )
        EmailThread(email_obj).start()

        return Response({"detail": "Password reset email sent"}, status=200)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import PasswordResetConfirmSerializer



class PasswordResetVerifyAPIView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response({"detail": "Token is required"}, status=400)

        # تبدیل token ورودی به hash قبل از سرچ در دیتابیس
        import hashlib
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        prt = PasswordResetToken.objects.filter(
            token_hash=token_hash, 
            is_used=False, 
            expires_at__gt=timezone.now()
        ).first()

        if not prt:
            return Response({"detail": "Invalid or expired token"}, status=400)

        return Response({"detail": "Token is valid"}, status=200)



class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        token = request.data.get("token")
        password = request.data.get("password")

        if not token or not password:
            return Response({"detail": "Token and new password are required"}, status=400)

        prt = PasswordResetToken.objects.filter(token=token, is_used=False).first()
        if not prt:
            return Response({"detail": "Invalid or expired token"}, status=400)

        user = prt.user
        user.set_password(password)
        user.save()

        prt.is_used = True
        prt.save()

        return Response({"detail": "Password has been reset successfully."}, status=200)

