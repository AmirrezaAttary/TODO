import hashlib
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from mail_templated import EmailMessage
from ...utils import EmailThread
from ....models import PasswordResetToken
from ..serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.utils import timezone

User = get_user_model()


class PasswordResetRequestAPIView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        raw_token, token_obj = PasswordResetToken.create_token(user)

        # لینک به صورت خودکار با دامنه سایت ساخته می‌شود
        reset_path = f"/accounts/api/v1/password-reset/confirm/{raw_token}"
        reset_link = request.build_absolute_uri(reset_path)

        email_obj = EmailMessage(
            'email/password_reset.tpl',
            {'reset_link': reset_link},
            'admin@admin.com',
            to=[email]
        )
        EmailThread(email_obj).start()

        return Response({"detail": "Password reset email sent"}, status=200)




class PasswordResetConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        # توکن را مستقیم از URL path می‌گیریم
        try:
            token_obj = PasswordResetToken.objects.get(token_hash=hashlib.sha256(token.encode()).hexdigest())
        except PasswordResetToken.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=400)

        if not token_obj.is_valid():
            return Response({"detail": "Token expired"}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=token_obj.user)

        # توکن یکبار مصرف باشد
        token_obj.delete()

        return Response({"detail": "Password has been reset successfully."}, status=200)



