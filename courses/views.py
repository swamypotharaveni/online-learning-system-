from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import CourseSerializer,CourseListSerializer
from datetime import datetime,timezone
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from.models import Course
from accounts.permissions import IsInstructor


class corsesview(APIView):
    permission_classes = [IsAuthenticated,IsInstructor]
    def get(self,request):
        print(request.user)
        courses=Course.objects.filter(instructor=request.user)
        serializer=CourseSerializer(courses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        data=request.data.copy()
        data['instructor']=request.user.id
        serializer=CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,pk):
        data=request.data.copy()
        data['instructor']=request.user.id
        course = get_object_or_404(Course, pk=pk)
        serializer=CourseSerializer(course,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class CourseInstructorDetails(APIView):
    permission_classes = [IsAuthenticated,IsInstructor]
    def get(self,request,pk):
        try:
            course=Course.objects.get(pk=pk,instructor=request.user)
            courserializer=CourseSerializer(course)
            return Response(courserializer.data,status=status.HTTP_200_OK)
        except Course.DoesNotExist as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
            
        
class AllCoursesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)