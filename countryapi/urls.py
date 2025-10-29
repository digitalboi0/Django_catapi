from django.urls import path
from . import views 

urlpatterns = [
    path('status/', views.GetCountryStatus.as_view(), name='country-status'),
    path('countries/refresh/', views.RefreshCountryView.as_view(), name='country-refresh'),
    path('countries/image/', views.GetImageSummery.as_view(), name='country-image'),
    path('countries/', views.GetCountriesView.as_view(), name='country-list'),
    path('countries/<str:name>/', views.GetCountryView.as_view(), name='country-detail'),
]