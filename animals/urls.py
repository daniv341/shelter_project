from rest_framework.routers import DefaultRouter

from animals.views import AnimalViewSet

router = DefaultRouter()
router.register("animals", AnimalViewSet, basename="animal")

urlpatterns = router.urls
