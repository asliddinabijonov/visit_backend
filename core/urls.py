from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ArtefaktViewSet,
    CommentViewSet,
    GidViewSet,
    ImageViewSet,
    LanguageViewSet,
    MehmonxonaViewSet,
    RestoranViewSet,
    TaomViewSet,
    TarixiyObidaViewSet,
    TransportTurViewSet,
    TransportViewSet,
    ViloyatViewSet,
    XususiyatViewSet,
)

router = DefaultRouter()
router.register("languages", LanguageViewSet)
router.register("images", ImageViewSet)
router.register("xususiyatlar", XususiyatViewSet)
router.register("transport-turlar", TransportTurViewSet)
router.register("viloyatlar", ViloyatViewSet)
router.register("tarixiy-obidalar", TarixiyObidaViewSet)
router.register("restoranlar", RestoranViewSet)
router.register("mehmonxonalar", MehmonxonaViewSet)
router.register("transportlar", TransportViewSet)
router.register("comments", CommentViewSet)
router.register("gidlar", GidViewSet)
router.register("artefaktlar", ArtefaktViewSet)
router.register("taomlar", TaomViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
