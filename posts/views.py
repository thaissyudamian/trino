from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Post
from .serializers import PostSerializer, RegisterSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
