from rest_framework.routers import DefaultRouter
from adoption_events.views import AdoptionEventViewSet

router = DefaultRouter()
router.register("adoption_events", AdoptionEventViewSet, basename="adoption_event")
urlpatterns = router.urls
