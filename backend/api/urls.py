from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.auth_views import SignInAPIView, SignUpAPIView, UpdateTokenAPIView
from .views.posts_views import NewsAddAPIViews, NewsCommentsAPIView, NewsListAPIView
from .views.roles_views import IsAdminAPIView, RoleListAPIView
from .views.user_views import ProfileAPIView

urlpatterns = [
    path("posts", NewsListAPIView.as_view(), name="posts-list"),
    path("posts/create", NewsAddAPIViews.as_view(), name="posts-add"),
    path("posts/comments", NewsCommentsAPIView.as_view(), name="posts-comments"),
    path("role/is-admin", IsAdminAPIView.as_view(), name="is-admin"),
    path("role/list", RoleListAPIView.as_view(), name="role-list"),
    path("auth/signup", SignUpAPIView.as_view(), name="sign-up"),
    path("auth/signin", SignInAPIView.as_view(), name="sign-in"),
    path("auth/refresh", UpdateTokenAPIView.as_view(), name="sign-in"),
    path("users/profile", ProfileAPIView.as_view(), name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
