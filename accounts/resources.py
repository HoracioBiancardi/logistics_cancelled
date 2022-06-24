from import_export import resources

from .models import PedidosCancelamento


class PedidosCancelamentosResource(resources.ModelResource):
    class Meta:
        model = PedidosCancelamento



