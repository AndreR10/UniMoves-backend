from .views import MessageEditView
from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('my-chat-messages', MessageEditView, basename='my-chat-messages')

urlpatterns = router.urls
