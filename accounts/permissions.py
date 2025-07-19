from rest_framework.permissions import BasePermission
class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated  and request.user.is_instructor
class is_student(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student
    