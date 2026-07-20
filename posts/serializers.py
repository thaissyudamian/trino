from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Follow, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "author", "content", "created_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source="follower.username")

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]

    def validate_following(self, value):
        user = self.context["request"].user
        if value == user:
            raise serializers.ValidationError("Você não pode seguir a si mesmo.")
        if Follow.objects.filter(follower=user, following=value).exists():
            raise serializers.ValidationError("Você já segue este usuário.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "created_at"]
        
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]

    def validate_post(self, value):
        user = self.context["request"].user
        if Like.objects.filter(user=user, post=value).exists():
            raise serializers.ValidationError("Você já curtiu este post.")
        return value


