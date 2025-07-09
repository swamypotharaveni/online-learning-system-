from rest_framework import serializers
from.models import Course,Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields=['id', 'title', 'description', 'video_url', 'video_file', 'order', 'is_preview']
class CourseSerializer(serializers.ModelSerializer):
    lessons=LessonSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'is_paid', 'thumbnail', 'category', 'created_at', 'instructor', 'lessons']
        
    def create(self, validated_data):
        print("Validated Data Keys:", validated_data.keys())
        lessons_data = validated_data.pop('lessons')
        course=Course.objects.create(**validated_data)
        for leassion_data in lessons_data:
            Lesson.objects.create(course=course, **leassion_data)
        return course
    def update(self, instance, validated_data):
        
        validated_data.pop('lessons', None)

        # Update only the desired fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)

        instance.save()
        return instance


class CourseListSerializer(serializers.ModelSerializer):
    instructor_name=serializers.CharField(source='instructor.username')
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'is_paid', 'thumbnail', 'category', 'created_at', 'instructor','instructor_name']
