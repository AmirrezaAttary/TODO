from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from ..serializers import RegistrationSerializer
from ...utils import EmailThread

User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'email':email
            }
            user_obj = get_object_or_404(User,email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com',to=[email])
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)