from django.urls import path
from . import views

urlpatterns = [
    path('me', views.Userprofile.as_view(), name="userprofile"),
    path('strings', views.create_string.as_view(), name='create_string'),
   # path('strings/<str:string_value>/', views.get_string.as_view(), name='get_string'), 
    path('strings/<str:string_value>/', views.delete_string.as_view(), name='delete_string'),
    path('strings/', views.string_list.as_view(), name='list_strings'), 
    
    path('strings/filter-by-natural-language', views.natural_lang.as_view(), name='filter_by_natural_language'),
]
