from rest_framework import serializers

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


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class XususiyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xususiyat
        fields = "__all__"


class TransportTurSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportTur
        fields = "__all__"


class ViloyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viloyat
        fields = "__all__"


class TarixiyObidaSerializer(serializers.ModelSerializer):
    images_detail = ImageSerializer(source="images", many=True, read_only=True)

    class Meta:
        model = TarixiyObida
        fields = "__all__"

    def validate(self, attrs):
        instance = TarixiyObida(**attrs)
        if self.instance:
            for field in (
                "viloyat",
                "title",
                "description",
                "location",
                "date",
                "cost",
                "video",
                "video_url",
                "video_poster",
                "video_type",
                "video_projection",
                "stereo_mode",
                "vr_ready",
                "video_duration_seconds",
            ):
                if field not in attrs:
                    setattr(instance, field, getattr(self.instance, field))
        instance.clean()
        return attrs


class RestoranSerializer(serializers.ModelSerializer):
    images_detail = ImageSerializer(source="images", many=True, read_only=True)
    xususiyat_detail = XususiyatSerializer(source="xususiyat", many=True, read_only=True)

    class Meta:
        model = Restoran
        fields = "__all__"
        read_only_fields = ("user",)


class MehmonxonaSerializer(serializers.ModelSerializer):
    images_detail = ImageSerializer(source="images", many=True, read_only=True)
    xususiyat_detail = XususiyatSerializer(source="xususiyat", many=True, read_only=True)

    class Meta:
        model = Mehmonxona
        fields = "__all__"
        read_only_fields = ("user",)


class TransportSerializer(serializers.ModelSerializer):
    image_detail = ImageSerializer(source="image", read_only=True)
    xususiyat_detail = XususiyatSerializer(source="xususiyat", read_only=True)
    transport_turi_detail = TransportTurSerializer(source="transport_turi", read_only=True)

    class Meta:
        model = Transport
        fields = "__all__"
        read_only_fields = ("user",)


class GidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gid
        fields = "__all__"
        read_only_fields = ("user",)


class ArtefaktSerializer(serializers.ModelSerializer):
    images_detail = ImageSerializer(source="images", many=True, read_only=True)

    class Meta:
        model = Artefakt
        fields = "__all__"


class TaomSerializer(serializers.ModelSerializer):
    images_detail = ImageSerializer(source="images", many=True, read_only=True)

    class Meta:
        model = Taom
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    target_label = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def validate(self, attrs):
        instance = Comment(**attrs)
        if self.instance:
            for field in (
                "user",
                "viloyat",
                "target_type",
                "content_type",
                "object_id",
                "comment",
                "rating",
            ):
                if field not in attrs:
                    setattr(instance, field, getattr(self.instance, field))
        instance.clean()
        return attrs


class TarixiyObidaFullSerializer(TarixiyObidaSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    artefaktlar = serializers.SerializerMethodField()

    class Meta(TarixiyObidaSerializer.Meta):
        pass

    def get_artefaktlar(self, obj):
        return ArtefaktSerializer(obj.artefaktlar.all(), many=True).data


class RestoranFullSerializer(RestoranSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    taomlar = serializers.SerializerMethodField()

    def get_taomlar(self, obj):
        return TaomSerializer(obj.taomlar.all(), many=True).data


class MehmonxonaFullSerializer(MehmonxonaSerializer):
    comments = CommentSerializer(many=True, read_only=True)


class TarixiyObidaFullSerializer(TarixiyObidaSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    artefaktlar = serializers.SerializerMethodField()

    class Meta(TarixiyObidaSerializer.Meta):
        pass

    def get_artefaktlar(self, obj):
        return ArtefaktSerializer(obj.artefaktlar.all(), many=True).data


class TransportFullSerializer(TransportSerializer):
    comments = CommentSerializer(many=True, read_only=True)


class GidFullSerializer(GidSerializer):
    comments = CommentSerializer(many=True, read_only=True)


class ViloyatFullSerializer(serializers.ModelSerializer):
    tarixiy_obidalar = TarixiyObidaFullSerializer(many=True, read_only=True)
    restoranlar = RestoranFullSerializer(many=True, read_only=True)
    mehmonxonalar = MehmonxonaFullSerializer(many=True, read_only=True)
    transportlar = TransportFullSerializer(many=True, read_only=True)
    gidlar = GidFullSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Viloyat
        fields = "__all__"
