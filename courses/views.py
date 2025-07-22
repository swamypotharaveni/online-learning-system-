from django.shortcuts import get_object_or_404, render
import razorpay.errors
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
from .models import CourseEnrollment,CoursePayment
import razorpay
from online_learning import settings


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
class EnrollFreeCourseView(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request):
        try:
            course=Course.objects.get(id=request.data['course_id'])
            if course.instructor ==request.user:
                 return Response({"details":"You cannot enroll in your own course."},status=status.HTTP_400_BAD_REQUEST)
                
            if course.is_paid:
                return Response({"details":"this paid course"},status=status.HTTP_400_BAD_REQUEST)
            enroll,created=CourseEnrollment.objects.get_or_create(user=request.user,course=course)
            if not created:
                return Response({"detail": f"You are already enrolled in {course.title}."},status=status.HTTP_400_BAD_REQUEST)
            return Response({"details":f"Successfully enrolled in {course.title}."},status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

class CreateRazorpayOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            course=Course.objects.get(id=request.data["course_id"])
            if course.instructor == request.user:
                return Response({"details":"You cannot enroll in your own course."},status=status.HTTP_400_BAD_REQUEST)
            if not course.is_paid:
                return Response({"details":"this free course"},status=status.HTTP_400_BAD_REQUEST)
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            order_data={
                      "amount":int(course.price * 100),
                        "currency": "INR",
                        "receipt":  f"order_rcptid_{course.id}_{request.user.id}"}
            try:
                order=client.order.create(data=order_data)
                print(order)
            except razorpay.errors.BadRequestError as e:
                return Response({"detail": "Failed to create order", "error": str(e)}, status=400)
            CoursePayment.objects.create(
                user=request.user,
                course=course,
                amount=course.price,
                status="PENDING",
                payment_id=order["id"])
            return Response({
                 "order_id":order['id'] ,
                "amount": course.price,
                "currency":"INR",
                "course_id":course.id ,
                "razorpay_key_id":settings.RAZORPAY_KEY_ID
                
            })
            
        except Course.DoesNotExist:
             return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
            

class VerifyRazorpayPaymentView(APIView):
    permission_classes = [IsAuthenticated]  # Change to IsAuthenticated for secure apps

    def post(self, request):
        try:
            data = request.data

            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response({"detail": "Missing payment fields"}, status=400)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            payment_sign = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(payment_sign)

            # Fetch payment object
            payment = CoursePayment.objects.get(payment_id=razorpay_order_id)
            payment.status = "SUCCESS"
            payment.payment_method = "Razorpay"
            payment.save()


            CourseEnrollment.objects.get_or_create(user=request.user, course=payment.course)

            return Response({"detail": "Payment verified and enrolled successfully!"}, status=200)

        except razorpay.errors.SignatureVerificationError:
            return Response({"detail": "Payment verification failed"}, status=400)

        except CoursePayment.DoesNotExist:
            return Response({"detail": "Payment record not found"}, status=404)
