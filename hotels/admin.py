from django import forms
from django.contrib import admin

from .models import Mehmonxona


class MehmonxonaForm(forms.ModelForm):
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
        model = Mehmonxona
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.kunlar:
            self.initial["kunlar"] = self.instance.kunlar.split(",")

    def clean_kunlar(self):
        data = self.cleaned_data.get("kunlar", [])
        return ",".join(data) if data else ""


@admin.register(Mehmonxona)
class MehmonxonaAdmin(admin.ModelAdmin):
    form = MehmonxonaForm
    list_display = ("id", "title", "viloyat", "user")
    list_filter = ("viloyat",)
    search_fields = ("title", "location")
    filter_horizontal = ("images", "xususiyat")
