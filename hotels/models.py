from core.models import Mehmonxona as CoreMehmonxona


class Mehmonxona(CoreMehmonxona):
    class Meta:
        proxy = True
        app_label = "hotels"
        verbose_name = "Mehmonxona"
        verbose_name_plural = "Mehmonxonalar"
