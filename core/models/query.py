from django.db import models
from django.db.models import Q


class ActiveQuerySet(models.QuerySet):
    """
    ActivatorQuerySet

    Query set that returns statused results
    """

    def active(self):
        """ Return active query set """
        return self.filter(is_active=True)

    def inactive(self):
        """ Return inactive query set """
        return self.filter(is_active=False)
    
