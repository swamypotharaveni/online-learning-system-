from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from .models import CourseEnrollment,CoursePayment

@receiver(post_save, sender=CourseEnrollment)
def send_enrollment_email(sender, instance, created, **kwargs):
    if created:
        lesstion=instance.course.lessons.all()
        print("lesstion", lesstion)
        for lesson in lesstion:
            if lesson.is_preview:
                print(f"Preview lesson available: {lesson.title} in course {instance.course.title}")
            else:
                print(f"Lesson {lesson.title} is not a preview in course {instance.course.title}")
        
        print(f"Enrollment created for {instance.user.username} in course {instance.course.title}")
@receiver(post_save, sender=CourseEnrollment)
def update_course_progress(sender, instance, created,**kwargs):
    if not created:
        print("instance", instance.id)
        print(f"Enrollment updated for {instance.user.username} in course {instance.course.title}")
@receiver(post_save, sender=CoursePayment)
def send_payment_confirmation(sender, instance, created, **kwargs):
    if created:
        print(f"Payment confirmed for {instance.user.username} in course {instance.course.title}")
    else:
        print(f"Payment updated for {instance.user.username} in course {instance.course.title}")