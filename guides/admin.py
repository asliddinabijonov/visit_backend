from django.contrib import admin

from .models import Gid


@admin.register(Gid)
class GidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "viloyat", "country", "language")
    list_filter = ("viloyat", "country")
    search_fields = ("user__username", "title", "country", "language")
