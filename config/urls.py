from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("animals.urls")),
    path("api/", include("caretakers.urls")),
    path("api/", include("adopters.urls")),
    path("api/", include("species.urls")),
    path("api/", include("veterinarians.urls")),
    path("api/", include("vaccination_records.urls")),
    path("api/", include("medical_treatments.urls")),
    path("api/", include("adoption_applications.urls")),
    # OpenAPI schema + Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
