"""urls"""

from rest_framework.routers import DefaultRouter
from src.apps.studio_session.api import views

router = DefaultRouter()
router.register(r'session',
                views.StudioSessionViewSet,
                basename='studio_session')
router.register(r'coordinator',
                views.StudioSessionCoordinatorViewSet,
                basename='studio_coordinator')
router.register(r'reservation',
                views.StudioSessionReservationViewSet,
                basename='studio_reservation')

urlpatterns = router.urls
app_name = 'studio'
