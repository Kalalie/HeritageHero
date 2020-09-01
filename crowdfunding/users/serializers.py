from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email  = serializers.CharField(max_length=200)
    full_name = serializers.CharField(max_length=200)
    display_picture = serializers.URLField(required=False)
    password = serializers.CharField(write_only=True, required=True)


    # def create(self, validated_data):
        # validated_data['password'] = make_password(validated_data.get('password'))
        # return CustomUser.objects.create(**validated_data)
    
    def create(self, validated_data):
        new_user = CustomUser.objects.create(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    
    