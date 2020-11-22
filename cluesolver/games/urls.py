from django.urls import path
from . import views

app_name = 'games'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/<int:pk>/', views.GameplayDashboardView.as_view(), name='gameplay-dashboard'),
]
