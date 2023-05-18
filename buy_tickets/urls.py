from django.urls import path, include
from .views import CategoryViewSet,AirLinesViewSet,AirTicketViewSet,CommentView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('category',CategoryViewSet)
router.register('airticket',AirTicketViewSet)
router.register('airlines',AirLinesViewSet)
router.register('comments',CommentView)

urlpatterns = [
    path('',include(router.urls))
]