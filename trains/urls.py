from rest_framework.routers import DefaultRouter
from .views import TrainViewSet, SeatViewSet

router = DefaultRouter()
router.register('trains', TrainViewSet, basename='train')
router.register('seats', SeatViewSet, basename='seat')

urlpatterns = router.urls