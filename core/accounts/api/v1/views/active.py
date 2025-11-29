import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidSignatureError,DecodeError
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from ..serializers import ActivationResendSerializer
from ...utils import EmailThread

User = get_user_model()

class ActivationApiView(APIView):
    def get(self,request,token,*args,**kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token['user_id']
        except ExpiredSignatureError:
            return Response({'detail':'Activation link has been expired'},status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'detail':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({'detail':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)
        
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({'detail':'your account already verified'},status=status.HTTP_200_OK)
        user_obj.is_verified = True
        user_obj.save()
        return Response({'detail':'your account verification'},status=status.HTTP_200_OK)
    
    
    
class ResendActivationEmailApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer
    
    def post(self,request,*args,**kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com',to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({'detail':'email sent successfully'},status=status.HTTP_200_OK)
                
        
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)