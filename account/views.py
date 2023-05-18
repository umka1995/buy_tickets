from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .permissions import IsActivePermissions
from .serializers import RegistrationSerializer, ActivationSerializer ,LoginSerializer ,ChangePasswordSerializer,ForgotPasswordSerializer,ForgotPasswordCompleteSerializer

class RegistrationView(APIView):
    def post(self,request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=200)

class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('Аккаунт успешно активирован',status=200)
    
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsActivePermissions]
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы вышли со своего аккаунта')

class ChangePasswordView(APIView):
    permission_classes = (IsActivePermissions,)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception = True):
            serializer.set_new_password()
            return Response('Status: 200. Пароль успешно обновлен')
        
class ForgotPasswordView(APIView):   
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.send_verification_email()
            return Response('Вы выслали сообщение для востановления')

class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.set_new_password()
            return Response('Пароль успешно изменен')
        









