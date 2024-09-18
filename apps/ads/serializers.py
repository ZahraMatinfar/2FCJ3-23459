from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.account.serializers import UserSerializer
from .models import Comment, Ad


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_time', 'updated_time']
        

    def validate(self, data):
        # Check if the user has already commented on the ad
        user = self.context["request"].user
        ad_pk = self.context.get('ad_pk')
        
        if ad_pk is None:
            raise serializers.ValidationError(_("ad_pk is required."))
        
        if user and user.comments.filter(ad=self.context["ad_pk"]).exists():
            raise serializers.ValidationError(_("You have already commented on this ad."))
        return data
    

class AdSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = ["id", "title", "description", "owner", "comments", "created_time", "updated_time"]

