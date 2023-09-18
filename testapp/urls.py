from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(prefix='poll', viewset=views.PollViewSet)
router.register(prefix='choice', viewset=views.ChoiceViewSet)
router.register(prefix='poll-history', viewset=views.PollHistoryViewSet)
router.register(prefix='choice-history', viewset=views.ChoiceHistoryViewSet)

app_name = 'test'

urlpatterns = [
    path(route=f'{app_name}/', view=include((router.urls, app_name), namespace=app_name)),
]
