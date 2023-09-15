from django.contrib import admin

from analytics.models import PostActivity


@admin.register(PostActivity)
class PostActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "action", "occurred_at")
