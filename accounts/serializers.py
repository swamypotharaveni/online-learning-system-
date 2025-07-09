from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()

class InstructorSignupSerializer(serializers.ModelSerializer):
    phone_number=serializers.CharField(allow_blank=True, required=False)
    class Meta:
        model=User
        fields=["username","email","password","phone_number"]
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        print(validated_data)
        phone_number=validated_data.pop('phone_number',None)
        user=User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_instructor=True
        user.phone_number=phone_number
        user.save()
        return user
class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id", "username", "email", "is_student", "is_instructor", "phone_number","last_login","is_active","date_joined"]
    
