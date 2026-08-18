from rest_framework.routers import DefaultRouter
from adoption_applications.views import AdoptionApplicationViewSet

router = DefaultRouter()
router.register("adoption_applications", AdoptionApplicationViewSet, basename="adoption_application")
urlpatterns = router.urls
