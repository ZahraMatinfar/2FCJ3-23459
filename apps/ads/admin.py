from django.contrib import admin
from apps.ads.models import Comment, Ad

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = (
        "pk",
        # "text",
    )


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "owner",
    )
    inlines = [CommentInline]
    search_fields = (
        "title",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )