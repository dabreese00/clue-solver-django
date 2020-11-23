from django.urls import path
from . import views

app_name = 'games'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/<int:game_id>/', views.gameplay_dashboard,
         name='gameplay-dashboard'),
    path('create_game/', views.create_game, name='create-game'),
]
