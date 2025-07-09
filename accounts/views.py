from django.shortcuts import render

# Create your views here.
# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import InstructorSignupSerializer,UserSerilizer
from datetime import datetime,timezone
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
class InstructorSignupView(APIView):
    def post(self, request):
        serializer = InstructorSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Instructor registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes=[AllowAny,]
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user=authenticate(username=username,password=password)
        if user:
            user.last_login=now()
            user.save()
            refresh=RefreshToken.for_user(user)
            token={
                "token_type": "Bearer",
                "access":str(refresh.access_token),
                "refresh":str(refresh)
                
            }
            user_data=UserSerilizer(user)
            return Response({"message": "Login successful","user": user_data.data,"token":token},status=status.HTTP_200_OK)
        return Response({ "message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
class Logout(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request):
        try:
            refresh=request.data['refresh_token']
            token=RefreshToken(refresh)
            token.blacklist()
            return Response({"message": "Logout successful"},status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
