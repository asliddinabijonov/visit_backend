from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Language(models.Model):
    country = models.CharField(max_length=100, blank=True, null=True)
    language_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="languages/", blank=True, null=True)

    def __str__(self):
        return self.language_name


class Image(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title or str(self.image)


class Xususiyat(models.Model):
    turi = models.CharField(max_length=100)

    def __str__(self):
        return self.turi


class TransportTur(models.Model):
    turi = models.CharField(max_length=100)

    def __str__(self):
        return self.turi


class Viloyat(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="viloyatlar/", blank=True, null=True)
    comments = GenericRelation("Comment", related_query_name="viloyat_target")

    def __str__(self):
        return self.name


class Gid(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gid_profile",
    )
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="gids/", blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    language_ref = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gidlar",
    )
    viloyat = models.ForeignKey(
        Viloyat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gidlar",
    )
    comments = GenericRelation("Comment", related_query_name="gid_target")

    def __str__(self):
        return f"Gid: {self.user}"


class TarixiyObida(models.Model):
    class VideoType(models.TextChoices):
        STANDARD = "standard", "Oddiy video"
        VIDEO_360 = "360", "360 video"

    class VideoProjection(models.TextChoices):
        EQUIRECTANGULAR = "equirectangular", "Equirectangular"
        CUBEMAP = "cubemap", "Cubemap"
        FISHEYE = "fisheye", "Fisheye"

    class StereoMode(models.TextChoices):
        MONO = "mono", "Mono"
        LEFT_RIGHT = "left_right", "Left-Right"
        TOP_BOTTOM = "top_bottom", "Top-Bottom"

    viloyat = models.ForeignKey(
        Viloyat,
        on_delete=models.CASCADE,
        related_name="tarixiy_obidalar",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.ManyToManyField(
        Image,
        blank=True,
        related_name="tarixiy_obidalar",
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    video = models.FileField(
        upload_to="videos/tarixiy_obidalar/",
        blank=True,
        null=True,
    )
    video_url = models.URLField(blank=True, null=True)
    video_poster = models.ImageField(
        upload_to="videos/posters/",
        blank=True,
        null=True,
    )
    video_type = models.CharField(
        max_length=20,
        choices=VideoType.choices,
        default=VideoType.STANDARD,
    )
    video_projection = models.CharField(
        max_length=30,
        choices=VideoProjection.choices,
        blank=True,
        null=True,
    )
    stereo_mode = models.CharField(
        max_length=20,
        choices=StereoMode.choices,
        default=StereoMode.MONO,
    )
    vr_ready = models.BooleanField(default=False)
    video_duration_seconds = models.PositiveIntegerField(blank=True, null=True)
    kunlar = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ish kunlari: dushanba,seshanba,chorshanba,payshanba,juma,shanba,yakshanba"
    )
    comments = GenericRelation("Comment", related_query_name="tarixiy_obida_target")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if self.video and self.video_url:
            raise ValidationError(
                {"video_url": "Faqat bitta video manbasini kiriting: fayl yoki URL."}
            )

        if self.vr_ready and self.video_type != self.VideoType.VIDEO_360:
            raise ValidationError(
                {"vr_ready": "VR rejim faqat 360 video uchun yoqilishi mumkin."}
            )

        if self.video_type == self.VideoType.VIDEO_360 and not self.video_projection:
            raise ValidationError(
                {"video_projection": "360 video uchun projection turi majburiy."}
            )


class Artefakt(models.Model):
    class Davr(models.TextChoices):
        ILK_TOSH_DEVOR = "ilk_tosh_devor", "Ilk Tosh Devr"
        jeMISL_JAMOASI = "jemisl_jamoasi", "Jemisl Jamoasi"
        QADIMGI_YUNON = "qadimgi_yunon", "Qadimgi Yunon"
        SAK = "sak", "Sak"
        PART = "part", "Part"
        SOGDIYANA = "sogdiana", "Sogdiana"
        XITOY = "xitoy", "Xitoy"
        ARAB = "arab", "Arab"
        MO_GOL = "mo_gol", "Mo'g'il"
        TEMURIYLAR = "temuriylar", "Temuriylar"
        SHAXRIZODA = "shaxrizoda", "Shahrizoda"

    tarixiy_obida = models.ForeignKey(
        TarixiyObida,
        on_delete=models.CASCADE,
        related_name="artefaktlar",
    )
    nomi = models.CharField(max_length=255)
    tavsif = models.TextField(blank=True, null=True)
    images = models.ManyToManyField(
        Image,
        blank=True,
        related_name="artefaktlar",
    )
    davr = models.CharField(
        max_length=30,
        choices=Davr.choices,
        blank=True,
        null=True)
    yoshi = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Yoshi yil bilan"
    )
    material = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Material: metall, loy, tosh, va h.k."
    )

    def __str__(self):
        return self.nomi


class Restoran(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="restoranlar",
    )
    viloyat = models.ForeignKey(
        Viloyat,
        on_delete=models.CASCADE,
        related_name="restoranlar",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.ManyToManyField(
        Image,
        blank=True,
        related_name="restoranlar",
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    xususiyat = models.ManyToManyField(
        Xususiyat,
        blank=True,
        related_name="restoranlar",
    )
    kunlar = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ish kunlari: dushanba,seshanba,chorshanba,payshanba,juma,shanba,yakshanba"
    )
    comments = GenericRelation("Comment", related_query_name="restoran_target")

    def __str__(self):
        return self.title


class Taom(models.Model):
    restoran = models.ForeignKey(
        Restoran,
        on_delete=models.CASCADE,
        related_name="taomlar",
    )
    nomi = models.CharField(max_length=255)
    tavsif = models.TextField(blank=True, null=True)
    images = models.ManyToManyField(
        Image,
        blank=True,
        related_name="taomlar",
    )
    narx = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nomi


class Mehmonxona(models.Model):
    class Kunlar(models.TextChoices):
        DUSHANBA = "dushanba", "Dushanba"
        SESHANBA = "seshanba", "Seshanba"
        CHORSHANBA = "chorshanba", "Chorshanba"
        PAYSHANBA = "payshanba", "Payshanba"
        JUMA = "juma", "Juma"
        SHANBA = "shanba", "Shanba"
        YAKSHANBA = "yakshanba", "Yakshanba"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mehmonxonalar",
    )
    viloyat = models.ForeignKey(
        Viloyat,
        on_delete=models.CASCADE,
        related_name="mehmonxonalar",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.ManyToManyField(
        Image,
        blank=True,
        related_name="mehmonxonalar",
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    xususiyat = models.ManyToManyField(
        Xususiyat,
        blank=True,
        related_name="mehmonxonalar",
    )
    kunlar = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ish kunlari: dushanba,seshanba,chorshanba,payshanba,juma,shanba,yakshanba"
    )
    comments = GenericRelation("Comment", related_query_name="mehmonxona_target")

    def __str__(self):
        return self.title


class Transport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transportlar",
    )
    viloyat = models.ForeignKey(
        Viloyat,
        on_delete=models.CASCADE,
        related_name="transportlar",
    )
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transportlar",
    )
    date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    xususiyat = models.ForeignKey(
        Xususiyat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transportlar",
    )
    transport_turi = models.ForeignKey(
        TransportTur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transportlar",
    )
    comments = GenericRelation("Comment", related_query_name="transport_target")

    def __str__(self):
        return self.title


class Comment(models.Model):
    class TargetType(models.TextChoices):
        VILOYAT = "viloyat", "Viloyat"
        RESTORAN = "restoran", "Restoran"
        MEHMONXONA = "mehmonxona", "Mehmonxona"
        TRANSPORT = "transport", "Transport"
        GID = "gid", "Gid"
        TARIXIY_OBIDA = "tarixiy_obida", "Tarixiy obida"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_comments",
    )
    viloyat = models.ForeignKey(
        "Viloyat",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="scoped_comments",
    )
    target_type = models.CharField(max_length=30, choices=TargetType.choices, blank=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to=models.Q(app_label="core", model__in=[
            "viloyat",
            "restoran",
            "mehmonxona",
            "transport",
            "gid",
            "tarixiyobida",
        ]),
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment #{self.pk}"

    @property
    def target_label(self):
        return str(self.content_object) if self.content_object else "-"

    def clean(self):
        super().clean()
        if not self.viloyat:
            raise ValidationError("Viloyat tanlanishi kerak.")

        if not self.content_type_id or not self.object_id:
            raise ValidationError("Comment uchun obyekt tanlanishi kerak.")

        target = self.content_object
        if target is None:
            raise ValidationError("Tanlangan obyekt topilmadi.")

        model_to_type = {
            Viloyat: self.TargetType.VILOYAT,
            Restoran: self.TargetType.RESTORAN,
            Mehmonxona: self.TargetType.MEHMONXONA,
            Transport: self.TargetType.TRANSPORT,
            Gid: self.TargetType.GID,
            TarixiyObida: self.TargetType.TARIXIY_OBIDA,
        }
        expected_type = model_to_type.get(type(target))
        if expected_type != self.target_type:
            raise ValidationError("Tanlangan obyekt turi noto'g'ri.")

        target_viloyat = getattr(target, "viloyat", None)
        if target_viloyat is not None and target_viloyat != self.viloyat:
            raise ValidationError("Tanlangan obyekt viloyatga mos emas.")
