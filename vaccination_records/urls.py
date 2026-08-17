from rest_framework.routers import DefaultRouter
from vaccination_records.views import VaccinationRecordViewSet

router = DefaultRouter()
router.register("vaccination_records", VaccinationRecordViewSet, basename="vaccination_record")
urlpatterns = router.urls
