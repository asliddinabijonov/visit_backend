from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

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
from .serializers import (
    ArtefaktSerializer,
    CommentSerializer,
    GidSerializer,
    ImageSerializer,
    LanguageSerializer,
    MehmonxonaSerializer,
    RestoranSerializer,
    TaomSerializer,
    TarixiyObidaSerializer,
    TransportSerializer,
    TransportTurSerializer,
    ViloyatSerializer,
    ViloyatFullSerializer,
    XususiyatSerializer,
)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)


class XususiyatViewSet(viewsets.ModelViewSet):
    queryset = Xususiyat.objects.all()
    serializer_class = XususiyatSerializer


class TransportTurViewSet(viewsets.ModelViewSet):
    queryset = TransportTur.objects.all()
    serializer_class = TransportTurSerializer


class ViloyatViewSet(viewsets.ModelViewSet):
    queryset = Viloyat.objects.all()
    serializer_class = ViloyatSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=True, methods=["get"], url_path="full", serializer_class=ViloyatFullSerializer)
    def full(self, request, pk=None):
        viloyat = (
            self.get_queryset()
            .prefetch_related(
                "tarixiy_obidalar",
                "tarixiy_obidalar__comments",
                "tarixiy_obidalar__images",
                "tarixiy_obidalar__artefaktlar",
                "tarixiy_obidalar__artefaktlar__images",
                "restoranlar",
                "restoranlar__comments",
                "restoranlar__images",
                "restoranlar__xususiyat",
                "restoranlar__taomlar",
                "restoranlar__taomlar__images",
                "mehmonxonalar",
                "mehmonxonalar__comments",
                "mehmonxonalar__images",
                "mehmonxonalar__xususiyat",
                "transportlar",
                "transportlar__comments",
                "gidlar",
                "gidlar__comments",
                "comments",
            )
            .get(pk=pk)
        )
        serializer = ViloyatFullSerializer(viloyat, context={"request": request})
        return Response(serializer.data)


class TarixiyObidaViewSet(viewsets.ModelViewSet):
    queryset = TarixiyObida.objects.all()
    serializer_class = TarixiyObidaSerializer
    parser_classes = (MultiPartParser, FormParser)


class OwnerManagedViewSet(viewsets.ModelViewSet):
    owner_field = "user"
    allowed_roles = ()
    single_profile = False

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy", "mine"}:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if (
            self.action in {"update", "partial_update", "destroy"}
            and self.request.user.is_authenticated
            and not self.request.user.is_staff
        ):
            return queryset.filter(**{self.owner_field: self.request.user})
        return queryset

    def _check_role(self):
        user = self.request.user
        if user.is_staff:
            return
        if user.role not in self.allowed_roles:
            raise PermissionDenied("Bu amal sizning role uchun ruxsat etilmagan.")

    def perform_create(self, serializer):
        self._check_role()
        if self.single_profile and self.get_queryset().filter(**{self.owner_field: self.request.user}).exists():
            raise ValidationError("Siz bu profilni allaqachon yaratgansiz.")
        serializer.save(**{self.owner_field: self.request.user})

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        self._check_role()
        queryset = self.get_queryset().filter(**{self.owner_field: request.user})
        if self.single_profile:
            instance = queryset.first()
            if not instance:
                return Response(None, status=status.HTTP_200_OK)
            return Response(self.get_serializer(instance).data)
        return Response(self.get_serializer(queryset, many=True).data)


class RestoranViewSet(OwnerManagedViewSet):
    queryset = Restoran.objects.all()
    serializer_class = RestoranSerializer
    allowed_roles = ("RESTAURANT_OWNER",)


class MehmonxonaViewSet(OwnerManagedViewSet):
    queryset = Mehmonxona.objects.all()
    serializer_class = MehmonxonaSerializer
    allowed_roles = ("HOTEL_OWNER",)


class TransportViewSet(OwnerManagedViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    allowed_roles = ("TAXI_OWNER",)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class GidViewSet(OwnerManagedViewSet):
    queryset = Gid.objects.all()
    serializer_class = GidSerializer
    allowed_roles = ("GUIDE",)
    single_profile = True
    parser_classes = (MultiPartParser, FormParser)


class ArtefaktViewSet(viewsets.ModelViewSet):
    queryset = Artefakt.objects.all()
    serializer_class = ArtefaktSerializer


class TaomViewSet(viewsets.ModelViewSet):
    queryset = Taom.objects.all()
    serializer_class = TaomSerializer
