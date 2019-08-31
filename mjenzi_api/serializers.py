from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Materials, Requests, Reports
from rest_framework.authtoken.models import Token


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = '__all__'


class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    materials = MaterialsSerializer(many=True, read_only=True, required=False)
    requests = RequestSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
