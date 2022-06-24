from django.db import models
from django.utils import timezone


class PedidosCancelamento(models.Model):
    id_pedido = models.CharField(max_length=50, blank=True, unique=True)
    nome_user = models.CharField(max_length=50,blank=True)
    motivo = models.TextField(max_length=200, blank=True)
    data_inclusao = models.DateTimeField(default=timezone.now)
    env_cancelamento = models.BooleanField(default=False)
    recarga_celular = models.BooleanField(default=False)
    corss_border = models.BooleanField(default=False)
    cash = models.BooleanField(default=False)
    status_not_cancel= models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.nome_user

