from rest_framework import serializers
from .models import User, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'is_accepted']
