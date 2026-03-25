from core.models import Transport as CoreTransport
from core.models import TransportTur as CoreTransportTur


class Transport(CoreTransport):
    class Meta:
        proxy = True
        app_label = "taxi"
        verbose_name = "Transport"
        verbose_name_plural = "Transportlar"


class TransportTur(CoreTransportTur):
    class Meta:
        proxy = True
        app_label = "taxi"
        verbose_name = "Transport turi"
        verbose_name_plural = "Transport turlari"
