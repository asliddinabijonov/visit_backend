from django.contrib import admin

from .models import Transport, TransportTur


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "viloyat", "transport_turi", "phone_number")
    list_filter = ("viloyat", "transport_turi")
    search_fields = ("title", "phone_number", "email")


@admin.register(TransportTur)
class TransportTurAdmin(admin.ModelAdmin):
    list_display = ("id", "turi")
    search_fields = ("turi",)
