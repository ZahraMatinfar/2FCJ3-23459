from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.ads import views

router = DefaultRouter()

router.register(r'', views.AdViewSet, basename='ad')

ads_urlpatterns = router.urls
ads_urlpatterns += [path('ads/<int:ad_pk>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name="comments"),]