from .views import ChatEditView
from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('my-chats', ChatEditView, basename='my-chats')

urlpatterns = router.urls
