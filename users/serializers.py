from rest_framework import serializers
from django.contrib.auth import get_user_model
from courses.models import Module
from .models import Follow
from rest_framework import serializers
from courses.models import Level, Speciality

class AssignModulesSerializer(serializers.Serializer):
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())
    speciality = serializers.PrimaryKeyRelatedField(queryset=Speciality.objects.all())


User = get_user_model()

# 🔐 Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
             'username', 'email', 'password',
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
            "id", "username", "email", "user_type",
            "bio", "background", "profile_photo",
            "speciality", "level", "modules"
        ]
        read_only_fields = ['id', 'username', 'email', 'user_type']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'speciality', 'level', 'profile_photo']

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type']


from rest_framework import serializers
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    professor_username = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'student', 'professor', 'professor_username', 'created_at']
        read_only_fields = ['student', 'professor','created_at']  # professor set manually

    def create(self, validated_data):
        request = self.context['request']
        student = request.user
        username = validated_data.pop('professor_username')

        try:
            professor = User.objects.get(username=username, user_type='professor')
        except User.DoesNotExist:
            raise serializers.ValidationError("❌ Professor with this username not found.")

        follow = Follow.objects.create(student=student, professor=professor)
        return follow

class FollowingSerializer(serializers.ModelSerializer):
    professor_username = serializers.CharField(source='professor.username', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'professor_username', 'created_at']



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'bio', 'background', 'profile_photo', 'speciality', 'level']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
