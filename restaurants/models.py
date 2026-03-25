from core.models import Restoran as CoreRestoran
from core.models import Taom as CoreTaom


class Restoran(CoreRestoran):
    class Meta:
        proxy = True
        app_label = "restaurants"
        verbose_name = "Restoran"
        verbose_name_plural = "Restoranlar"


class Taom(CoreTaom):
    class Meta:
        proxy = True
        app_label = "restaurants"
        verbose_name = "Taom"
        verbose_name_plural = "Taomlar"
