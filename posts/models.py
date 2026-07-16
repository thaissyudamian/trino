from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"
class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_like"
            )
        ]

    def __str__(self):
        return f"{self.user.username} curtiu post {self.post.id}"
class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow"
            ),
            models.CheckConstraint(
                condition=~models.Q(follower=models.F("following")),
                name="no_self_follow",
            ),
        ]

    def __str__(self):
        return f"{self.follower.username} segue {self.following.username}"
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.CharField(max_length=160, blank=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)

    def __str__(self):
        return self.user.username
