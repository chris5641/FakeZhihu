from rest_framework import serializers

from .models import Comment
from users.serializers import UserImageSerializer


class ReplySerializer(serializers.ModelSerializer):
    author = UserImageSerializer()

    class Meta:
        model = Comment
        fields = ('content', 'author', 'answer', 'create_time')


class CommentSerializer(serializers.ModelSerializer):
    author = UserImageSerializer()
    reply_to = ReplySerializer()
    create_time = serializers.DateTimeField(format='%m-%d %H:%M')

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'reply_to', 'answer', 'create_time')
