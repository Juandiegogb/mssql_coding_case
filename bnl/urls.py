from django.urls import path
from .base.views import LoginView, PayrollView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger", SpectacularSwaggerView.as_view(url_name="schema")),
    path("login", LoginView.as_view()),
    path("getPayments", PayrollView.as_view()),
    path("getPayments/<str:area>", PayrollView.as_view()),
]
