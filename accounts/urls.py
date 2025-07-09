from django.urls import path
from .views import InstructorSignupView,LoginView,Logout
urlpatterns = [
     path('instructor/signup/', InstructorSignupView.as_view(), name='instructor-signup'),
      path('login/', LoginView.as_view(), name='login'),
      path('logout/',Logout.as_view(),name="logout")
]
