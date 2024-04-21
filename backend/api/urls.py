from django.urls import path, include
from .views import *
urlpatterns = [
    path('auth/signup', UserAPIView.as_view(), name='sign-up'),
]

# path('auth/signup', SignUpAPIView.as_view(), name='sign-up'),