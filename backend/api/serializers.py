from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AdminUser, JobseekerCV, Question
import json

class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['username', 'email', 'password', 'role']  # ✅ Include role
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AdminUser.objects.create_user(**validated_data)
        return user

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user  # ✅ Will include user.role in view response
        raise serializers.ValidationError("Invalid credentials")

class JobseekerCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobseekerCV
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['education', 'scholarships', 'family', 'employment', 'references']:
            value = data.get(field)
            if value:
                try:
                    data[field] = json.loads(value)
                except json.JSONDecodeError:
                    pass
        return data

    def to_internal_value(self, data):
        for field in ['education', 'scholarships', 'family', 'employment', 'references']:
            if field in data and isinstance(data[field], (dict, list)):
                data[field] = json.dumps(data[field])
        return super().to_internal_value(data)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'