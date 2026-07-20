from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Follow, Comment, Like, Profile


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
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = ["id", "username", "name", "bio", "photo"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        if "first_name" in user_data:
            instance.user.first_name = user_data["first_name"]
            instance.user.save()
        return super().update(instance, validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user



