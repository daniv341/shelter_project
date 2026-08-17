from rest_framework.routers import DefaultRouter
from species.views import SpeciesViewSet

router = DefaultRouter()
router.register("species", SpeciesViewSet, basename="species")
urlpatterns = router.urls
