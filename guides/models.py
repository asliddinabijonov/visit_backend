from core.models import Gid as CoreGid


class Gid(CoreGid):
    class Meta:
        proxy = True
        app_label = "guides"
        verbose_name = "Gid"
        verbose_name_plural = "Gidlar"
