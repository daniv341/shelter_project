from rest_framework.routers import DefaultRouter
from adopters.views import AdopterViewSet

router = DefaultRouter()
router.register("adopters", AdopterViewSet, basename="adopter")
urlpatterns = router.urls
