from rest_framework.routers import SimpleRouter, DefaultRouter

from api.views import TaskViewSet, ProjectViewSet


router = DefaultRouter()
router.register('task', TaskViewSet, base_name='book')
router.register('project', ProjectViewSet, base_name='reader')


urlpatterns = router.urls
