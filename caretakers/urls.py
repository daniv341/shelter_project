from rest_framework.routers import DefaultRouter
from caretakers.views import CaretakerViewSet

router = DefaultRouter()
router.register("caretakers", CaretakerViewSet, basename="caretaker")
urlpatterns = router.urls
