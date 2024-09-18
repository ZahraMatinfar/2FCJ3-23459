"""
V1 api routers
"""
from django.urls import (
    include,
    path,
)
from rest_framework import routers

from .account.router import account_urlpatterns
from .ads.router import ads_urlpatterns

ROUTER = routers.DefaultRouter()

urlpatterns = [
    path("account/", include(account_urlpatterns)),
    path("ads/", include(ads_urlpatterns)),
]

urlpatterns += ROUTER.urls
