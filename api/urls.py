from django.urls import path
from . import views

urlpatterns = [
    path('me', views.Userprofile.as_view(), name="userprofile"),
]
