from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=150)
    stack = serializers.CharField(max_length=150)

class ProfileSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=255)
    user = UserSerializer()
    timestamp = serializers.CharField(max_length=100)
    fact = serializers.CharField()
