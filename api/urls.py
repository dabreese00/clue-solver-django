from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'cardsets', views.CardSetViewSet)
router.register(r'games', views.GameViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'gamecards', views.GameCardViewSet)
router.register(r'cluerelations', views.ClueRelationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
]
