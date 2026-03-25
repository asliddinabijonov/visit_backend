from django import forms
from django.contrib import admin

from .models import Artefakt, TarixiyObida


class TarixiyObidaForm(forms.ModelForm):
    kunlar = forms.MultipleChoiceField(
        required=False,
        choices=[
            ("dushanba", "Dushanba"),
            ("seshanba", "Seshanba"),
            ("chorshanba", "Chorshanba"),
            ("payshanba", "Payshanba"),
            ("juma", "Juma"),
            ("shanba", "Shanba"),
            ("yakshanba", "Yakshanba"),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Ish kunlari",
    )

    class Meta:
        model = TarixiyObida
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.kunlar:
            self.initial["kunlar"] = self.instance.kunlar.split(",")

    def clean_kunlar(self):
        data = self.cleaned_data.get("kunlar", [])
        return ",".join(data) if data else ""


@admin.register(TarixiyObida)
class TarixiyObidaAdmin(admin.ModelAdmin):
    form = TarixiyObidaForm
    list_display = ("id", "title", "viloyat", "video_type", "vr_ready")
    list_filter = ("viloyat", "video_type", "vr_ready", "stereo_mode")
    search_fields = ("title", "location", "description", "video_url")
    filter_horizontal = ("images",)
    fieldsets = (
        (
            "Asosiy ma'lumotlar",
            {"fields": ("viloyat", "title", "description", "images", "location", "kunlar", "cost")},
        ),
        (
            "Video va VR",
            {
                "fields": (
                    "video",
                    "video_url",
                    "video_poster",
                    "video_type",
                    "video_projection",
                    "stereo_mode",
                    "vr_ready",
                    "video_duration_seconds",
                )
            },
        ),
    )


@admin.register(Artefakt)
class ArtefaktAdmin(admin.ModelAdmin):
    list_display = ("id", "nomi", "tarixiy_obida", "davr", "yoshi", "material")
    list_filter = ("davr", "material", "tarixiy_obida__viloyat")
    search_fields = ("nomi", "tavsif")
    filter_horizontal = ("images",)

    class Media:
        js = ("core/admin/clipboard-paste.js",)
