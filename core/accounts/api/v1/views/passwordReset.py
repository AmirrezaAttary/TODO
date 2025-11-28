from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from mail_templated import EmailMessage
from ...utils import EmailThread
from ....models import PasswordResetToken
from ..serializers import PasswordResetRequestSerializer

User = get_user_model()


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        raw_token, token_obj = PasswordResetToken.create_token(user)

        reset_link = f"http://127.0.0.1:8000/reset-password/?token={raw_token}"

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

class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully"}, status=200)
