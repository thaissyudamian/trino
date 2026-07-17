from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, RegisterView

router = DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = router.urls + [
    path("register/", RegisterView.as_view()),
    path("login/", obtain_auth_token),
]
