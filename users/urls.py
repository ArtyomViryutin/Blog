from django.urls import path

from django.contrib.auth import urls

from .views import SignUp


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup')
]
