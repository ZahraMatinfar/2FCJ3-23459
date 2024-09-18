from django.urls import (
    include,
    path,
)

from .v1.router import urlpatterns as v1_urlpatterns

urlpatterns = [path("v1/", include(v1_urlpatterns))]
