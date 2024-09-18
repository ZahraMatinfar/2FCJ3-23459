from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models.base import BaseModel


User = get_user_model()


class Ad(BaseModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    owner = models.ForeignKey(
        verbose_name=_("Owner"), 
        to=User, 
        related_name='ads', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Ad")
        verbose_name_plural = _("Ads")
    

class Comment(BaseModel):
    ad = models.ForeignKey(
        verbose_name=_("Ad"),
        to=Ad, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name=_("User"),
        to=User, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    text = models.TextField(_("Text"))

    def __str__(self):
        return f"Comment by {self.user} on {self.ad}"
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        constraints = [
            models.UniqueConstraint(fields=['ad', 'user'], name='unique_comment_per_ad_user')
        ]

