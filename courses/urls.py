from django.urls import path
from .views import corsesview,AllCoursesView,CourseInstructorDetails
urlpatterns = [
     path('instructor/courses/', corsesview.as_view(), name='instructor_courses'),
     path('instructor/create_courses/', corsesview.as_view(), name='instructor_create_courses'),
     path('courses_instructor/<int:pk>/update/', corsesview.as_view(), name='instructor_update_course'),
     path('courses_instructor/<int:pk>/', CourseInstructorDetails.as_view(), name='instructor_course_details'),
     path('all_courser/', AllCoursesView.as_view(), name='all_courser'),
    
  
  
]
