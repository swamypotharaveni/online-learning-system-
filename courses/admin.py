from django.contrib import admin

# Register your models here.
from.models import Course,Lesson,CourseEnrollment

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'price', 'is_paid', 'created_at')
    inlines = [LessonInline]
    
admin.site.register(CourseEnrollment)
