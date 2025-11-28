from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from ...utils import EmailThread


User = get_user_model()


class TestEmailSend(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        self.email = "amir@amir.com"
        user_obj = get_object_or_404(User,email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'admin@admin.com',to=[self.email])
        EmailThread(email_obj).start()
        return Response({'detail':'email sent successfully'},status=status.HTTP_200_OK)
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)