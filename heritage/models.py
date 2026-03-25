from core.models import Artefakt as CoreArtefakt
from core.models import TarixiyObida as CoreTarixiyObida


class TarixiyObida(CoreTarixiyObida):
    class Meta:
        proxy = True
        app_label = "heritage"
        verbose_name = "Tarixiy obida"
        verbose_name_plural = "Tarixiy obidalar"


class Artefakt(CoreArtefakt):
    class Meta:
        proxy = True
        app_label = "heritage"
        verbose_name = "Artefakt"
        verbose_name_plural = "Artefaktlar"
