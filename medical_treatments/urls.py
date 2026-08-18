from rest_framework.routers import DefaultRouter
from medical_treatments.views import MedicalTreatmentViewSet

router = DefaultRouter()
router.register("medical_treatments", MedicalTreatmentViewSet, basename="medical_treatment")
urlpatterns = router.urls
