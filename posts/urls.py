from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, RegisterView, FollowViewSet, FeedView, CommentViewSet, LikeViewSet



router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("follows", FollowViewSet, basename="follow")
router.register("comments", CommentViewSet)
router.register("likes", LikeViewSet, basename="like")





urlpatterns = router.urls + [
    path("register/", RegisterView.as_view()),
    path("login/", obtain_auth_token),
    path("feed/", FeedView.as_view()),
]
