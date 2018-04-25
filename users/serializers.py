from rest_framework import serializers

from .models import User


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'nickname', 'sex', 'intro', 'work', 'get_image_url')


class UserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'nickname', 'get_image_url')

