from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post


class GetUserSerializer(serializers.ModelSerializer):
    """
    Get users info
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class PostSerializer(serializers.ModelSerializer):
    """
    Get and edit posts
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'user', 'create_time')


class ListPostSerializer(serializers.ModelSerializer):
    """
    Posts' list
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'user', 'create_time')