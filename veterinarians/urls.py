from rest_framework.routers import DefaultRouter
from veterinarians.views import VeterinarianViewSet

router = DefaultRouter()
router.register("veterinarians", VeterinarianViewSet, basename="veterinarian")
urlpatterns = router.urls
