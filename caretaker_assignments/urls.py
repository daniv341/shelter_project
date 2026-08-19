from rest_framework.routers import DefaultRouter
from caretaker_assignments.views import CaretakerAssignmentViewSet

router = DefaultRouter()
router.register("caretaker_assignments", CaretakerAssignmentViewSet, basename="caretaker_assignment")
urlpatterns = router.urls
