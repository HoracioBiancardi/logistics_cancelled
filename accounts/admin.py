from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import PedidosCancelamento


@admin.register(PedidosCancelamento)
class PedidosCancelamentoAdmin(ImportExportModelAdmin):
    list_display = ('id_pedido','nome_user','motivo','data_inclusao','env_cancelamento','corss_border','cash','status_not_cancel'
)

