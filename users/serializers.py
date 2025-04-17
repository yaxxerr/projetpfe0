from rest_framework import serializers
from django.contrib.auth import get_user_model
from courses.models import Module


User = get_user_model()

# 🔐 Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'user_type', 'level', 'speciality'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            level=validated_data.get('level'),
            speciality=validated_data.get('speciality'),
        )
        return user


# 👤 User detail serializer
class UserSerializer(serializers.ModelSerializer):
    level = serializers.StringRelatedField()
    speciality = serializers.StringRelatedField()
    modules = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'level', 'speciality', 'profile_photo',
            'bio', 'modules'
        ]
