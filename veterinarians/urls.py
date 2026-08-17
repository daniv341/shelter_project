from rest_framework.routers import DefaultRouter
from veterinarians.views import VeterinatianViewSet

router = DefaultRouter()
router.register("veterinarians", VeterinatianViewSet, basename="veterinatian")
urlpatterns = router.urls
