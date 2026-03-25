from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.urls import path, reverse


class HaftaKunlariWidget(forms.CheckboxSelectMultiple):
    KUNLAR = [
        ('dushanba', 'Dushanba'),
        ('seshanba', 'Seshanba'),
        ('chorshanba', 'Chorshanba'),
        ('payshanba', 'Payshanba'),
        ('juma', 'Juma'),
        ('shanba', 'Shanba'),
        ('yakshanba', 'Yakshanba'),
    ]
    
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.KUNLAR
        super().__init__(*args, **kwargs)


class HaftaKunlariField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = HaftaKunlariWidget.KUNLAR
        kwargs['widget'] = HaftaKunlariWidget()
        super().__init__(*args, **kwargs)
    
    def to_python(self, value):
        if not value:
            return ''
        if isinstance(value, list):
            return ','.join(value)
        return value


from .models import (
    Artefakt,
    Comment,
    Gid,
    Image,
    Language,
    Mehmonxona,
    Restoran,
    Taom,
    TarixiyObida,
    Transport,
    TransportTur,
    Viloyat,
    Xususiyat,
)


class TarixiyObidaForm(forms.ModelForm):
    kunlar = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('dushanba', 'Dushanba'),
            ('seshanba', 'Seshanba'),
            ('chorshanba', 'Chorshanba'),
            ('payshanba', 'Payshanba'),
            ('juma', 'Juma'),
            ('shanba', 'Shanba'),
            ('yakshanba', 'Yakshanba'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Ish kunlari"
    )
    
    class Meta:
        model = TarixiyObida
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.kunlar:
            self.initial['kunlar'] = self.instance.kunlar.split(',')
    
    def clean_kunlar(self):
        data = self.cleaned_data.get('kunlar', [])
        return ','.join(data) if data else ''


class TaomInline(admin.TabularInline):
    model = Taom
    extra = 1
    fields = ("nomi", "tavsif", "narx", "category")


COMMENT_TARGET_MODELS = {
    Comment.TargetType.RESTORAN: Restoran,
    Comment.TargetType.MEHMONXONA: Mehmonxona,
    Comment.TargetType.TRANSPORT: Transport,
    Comment.TargetType.GID: Gid,
    Comment.TargetType.TARIXIY_OBIDA: TarixiyObida,
}


class CommentAdminForm(forms.ModelForm):
    target_object = forms.ChoiceField(label="Obyekt", required=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content_type"].widget = forms.HiddenInput()
        self.fields["object_id"].widget = forms.HiddenInput()
        self.fields["target_type"].choices = [
            (target_type, label)
            for target_type, label in self.fields["target_type"].choices
            if target_type and target_type != Comment.TargetType.VILOYAT
        ]

        viloyat_id = self.data.get("viloyat") or getattr(self.instance, "viloyat_id", None)
        current_target_type = self.data.get("target_type") or getattr(self.instance, "target_type", "")
        current_object_id = self.data.get("object_id") or getattr(self.instance, "object_id", "")

        self.fields["target_object"].choices = self._build_target_choices(viloyat_id)

        if current_target_type and current_object_id:
            self.initial["target_object"] = f"{current_target_type}:{current_object_id}"

    def _build_target_choices(self, viloyat_id):
        choices = [("", "---------")]
        for target_type, model in COMMENT_TARGET_MODELS.items():
            queryset = model.objects.all()
            if viloyat_id:
                queryset = queryset.filter(viloyat_id=viloyat_id)
            choices.extend(
                (f"{target_type}:{obj.pk}", f"{model._meta.verbose_name.title()}: {obj}")
                for obj in queryset
            )
        return choices

    def clean(self):
        cleaned_data = super().clean()
        target_object_value = cleaned_data.get("target_object")

        if not target_object_value:
            raise ValidationError("Obyekt tanlanishi kerak.")

        try:
            target_type, target_object_id = target_object_value.split(":", 1)
        except ValueError as exc:
            raise ValidationError("Obyekt formati noto'g'ri.") from exc

        model = COMMENT_TARGET_MODELS.get(target_type)
        if not model:
            raise ValidationError("Noto'g'ri obyekt turi.")

        try:
            obj = model.objects.get(pk=target_object_id)
        except model.DoesNotExist as exc:
            raise ValidationError("Tanlangan obyekt topilmadi.") from exc

        cleaned_data["target_type"] = target_type
        cleaned_data["content_type"] = ContentType.objects.get_for_model(model)
        cleaned_data["object_id"] = obj.pk
        self.instance.target_type = target_type
        self.instance.content_type = cleaned_data["content_type"]
        self.instance.object_id = obj.pk
        return cleaned_data


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ("id", "user", "viloyat", "target_type", "target_label", "rating", "created_at")
    list_filter = ("target_type", "viloyat", "rating", "created_at")
    search_fields = ("user__username", "comment")
    fields = (
        "user",
        "viloyat",
        "target_type",
        "target_object",
        "content_type",
        "object_id",
        "comment",
        "rating",
        "created_at",
    )
    readonly_fields = ("created_at",)

    class Media:
        js = ("core/admin/comment-filter.js",)

    def get_urls(self):
        urls = super().get_urls()
        return urls


admin.site.register(Language)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "used_in")
    search_fields = ("title", "image")

    class Media:
        js = ("core/admin/clipboard-paste.js",)

    def used_in(self, obj):
        parts = []
        if obj.restoranlar.exists():
            parts.append(f"Restoran: {obj.restoranlar.count()}")
        if obj.mehmonxonalar.exists():
            parts.append(f"Mehmonxona: {obj.mehmonxonalar.count()}")
        if obj.tarixiy_obidalar.exists():
            parts.append(f"Obida: {obj.tarixiy_obidalar.count()}")
        if obj.transportlar.exists():
            parts.append(f"Transport: {obj.transportlar.count()}")
        return ", ".join(parts) or "-"

    used_in.short_description = "Tegishli obyektlar"


admin.site.register(Xususiyat)
admin.site.register(Viloyat)


class TarixiyObidaAdmin(admin.ModelAdmin):
    form = TarixiyObidaForm
    list_display = ("id", "title", "viloyat", "video_type", "vr_ready")
    list_filter = ("viloyat", "video_type", "vr_ready", "stereo_mode")
    search_fields = ("title", "location", "description", "video_url")
    filter_horizontal = ("images",)
    fieldsets = (
        (
            "Asosiy ma'lumotlar",
            {
                "fields": (
                    "viloyat",
                    "title",
                    "description",
                    "images",
                    "location",
                    "kunlar",
                    "cost",
                )
            },
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


class RestoranForm(forms.ModelForm):
    kunlar = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('dushanba', 'Dushanba'),
            ('seshanba', 'Seshanba'),
            ('chorshanba', 'Chorshanba'),
            ('payshanba', 'Payshanba'),
            ('juma', 'Juma'),
            ('shanba', 'Shanba'),
            ('yakshanba', 'Yakshanba'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Ish kunlari"
    )
    
    class Meta:
        model = Restoran
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.kunlar:
            self.initial['kunlar'] = self.instance.kunlar.split(',')
    
    def clean_kunlar(self):
        data = self.cleaned_data.get('kunlar', [])
        return ','.join(data) if data else ''


class MehmonxonaForm(forms.ModelForm):
    kunlar = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('dushanba', 'Dushanba'),
            ('seshanba', 'Seshanba'),
            ('chorshanba', 'Chorshanba'),
            ('payshanba', 'Payshanba'),
            ('juma', 'Juma'),
            ('shanba', 'Shanba'),
            ('yakshanba', 'Yakshanba'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Ish kunlari"
    )
    
    class Meta:
        model = Mehmonxona
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.kunlar:
            self.initial['kunlar'] = self.instance.kunlar.split(',')
    
    def clean_kunlar(self):
        data = self.cleaned_data.get('kunlar', [])
        return ','.join(data) if data else ''


class RestoranAdmin(admin.ModelAdmin):
    form = RestoranForm
    list_display = ("id", "title", "viloyat", "user")
    list_filter = ("viloyat",)
    search_fields = ("title", "location")
    filter_horizontal = ("images", "xususiyat")


class MehmonxonaAdmin(admin.ModelAdmin):
    form = MehmonxonaForm
    list_display = ("id", "title", "viloyat", "user")
    list_filter = ("viloyat",)
    search_fields = ("title", "location")
    filter_horizontal = ("images", "xususiyat")


class ArtefaktAdmin(admin.ModelAdmin):
    list_display = ("id", "nomi", "tarixiy_obida", "davr", "yoshi", "material")
    list_filter = ("davr", "material", "tarixiy_obida__viloyat")
    search_fields = ("nomi", "tavsif")
    filter_horizontal = ("images",)

    class Media:
        js = ("core/admin/clipboard-paste.js",)


class TaomAdmin(admin.ModelAdmin):
    list_display = ("id", "nomi", "restoran", "narx", "category")
    list_filter = ("category", "restoran__viloyat")
    search_fields = ("nomi", "tavsif")
    filter_horizontal = ("images",)
