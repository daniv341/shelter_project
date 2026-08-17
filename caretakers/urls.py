from rest_framework.routers import DefaultRouter
from caretakers.views import CaretakerViewSet

# se crea un router para registrar el viewset de caretakers y generar automáticamente las URLs para las acciones del viewset
router = DefaultRouter()
router.register("caretakers", CaretakerViewSet, basename="caretaker")
urlpatterns = router.urls
