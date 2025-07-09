from django.urls import path
from .views import corsesview,AllCoursesView
urlpatterns = [
     path('instructor/courses/', corsesview.as_view(), name='instructor-courses'),
     path('instructor/create_courses/', corsesview.as_view(), name='create_courses'),
     path('all_courser/', AllCoursesView.as_view(), name='all_courser'),
     path('courses/<int:pk>/update/', corsesview.as_view(), name='update-course'),
  
  
]
