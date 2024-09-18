from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.ads.models import Ad, Comment
from apps.ads.serializers import AdSerializer, CommentSerializer
from apps.ads.permissions import IsOwnerOrReadOnly
from drf_spectacular.utils import extend_schema


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related("owner").prefetch_related("comments").all().order_by("-created_time", "-updated_time")
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        return super().get_object()

    def perform_create(self, serializer):
        # The owner is automatically set to the logged-in user
        serializer.save(owner=self.request.user)

    @extend_schema(responses=AdSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['ad_pk'] = self.kwargs['ad_pk']  # Include ad_pk in the context
        return context

    def get_queryset(self):
        return Comment.objects.select_related("user").filter(ad=self.kwargs['ad_pk']).order_by("-created_time", "-updated_time")

    def perform_create(self, serializer):
        ad = get_object_or_404(Ad, pk=self.kwargs['ad_pk'])
        serializer.save(ad=ad, user=self.request.user)

    @extend_schema(responses=CommentSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
