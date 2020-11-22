from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/<int:id>/', views.GameplayDashboardView.as_view(), name='gameplay-dashboard'),
]
