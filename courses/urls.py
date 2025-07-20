from django.urls import path
from .views import corsesview,AllCoursesView,CourseInstructorDetails,EnrollFreeCourseView,CreateRazorpayOrderView,VerifyRazorpayPaymentView
urlpatterns = [
     path('instructor/courses/', corsesview.as_view(), name='instructor_courses'),
     path('instructor/create_courses/', corsesview.as_view(), name='instructor_create_courses'),
     path('courses_instructor/<int:pk>/update/', corsesview.as_view(), name='instructor_update_course'),
     path('courses_instructor/<int:pk>/', CourseInstructorDetails.as_view(), name='instructor_course_details'),
     path('all_courser/', AllCoursesView.as_view(), name='all_courser'),
     path("courses/enroll/free/",EnrollFreeCourseView.as_view(),name="courses/enroll/free/"),
      path('create_order/', CreateRazorpayOrderView.as_view(), name='create-razorpay-order'),
      path('verify-payment/', VerifyRazorpayPaymentView.as_view(), name='verify-razorpay-payment'),
]
