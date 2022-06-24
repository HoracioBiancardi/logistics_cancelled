import os
from sqlite3 import Row

import numpy as np
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./accounts/facily-817c2-4c57997e4983.json"
class RegrasCancelamento:
    def __init__(self) -> None:
        self.client = bigquery.Client()

    def env_cancelamento(self, pedidos):
        query=f"""
        select pedido 
        from `facily-817c2.facily_wp_logistic_aux.TB_ped_enviado_cancelamento` 
        where cast(pedido as string) in {pedidos}
        """
        dados = self.client.query(query).result().to_dataframe(create_bqstorage_client=True).pedido.values
        dados_cancelado = np.array(list(map(str, dados)))
        # dados_n_cancelado = np.setdiff1d(np.array(pedidos),dados_cancelado)
        return list(dados_cancelado)


    def cross_border(self, pedidos):
        query=f"""

        select pedido
        from `facily-817c2.facily_wp_logistic.log_pedidos_logistica` 
        where cast(pedido as string) in {pedidos} 
        and safe_cast(id_filial as INT64) in (97321472,97254276,71893174,70637894,73434034,68375042,69695432,69632218,65829734,66363252,72061147,66193890,85633500,121850703,76220405,53603282,110004908,68406778,
                                          71431645,72089320,66296625,94637473)
        """
        dados = self.client.query(query).result().to_dataframe(create_bqstorage_client=True).pedido.values
        dados_cross= np.array(list(map(str, dados)))
        #dados_n_cross = np.setdiff1d(np.array(pedidos),dados_cross)
        return list(dados_cross)


    def cash(self, pedidos):
        query=f"""
        select pedido
        from `facily-817c2.facily_wp_logistic.log_pedidos_logistica` 
        where cast(pedido as string) in {pedidos} 
        and safe_cast(id_filial as INT64) in (97321472,97254276,71893174,70637894,73434034,68375042,69695432,69632218,65829734,66363252,72061147,66193890,85633500,121850703,76220405,53603282,110004908,68406778,
                                          71431645,72089320,66296625,94637473)
        """
        dados = self.client.query(query).result().to_dataframe(create_bqstorage_client=True).pedido.values
        dados_cash= np.array(list(map(str, dados)))
        #dados_n_cash = np.setdiff1d(np.array(pedidos),dados_cash)
        return list(dados_cash)

    def recarga_celular(self, pedidos):
        query=f"""
        select
        'PEDIDOS RECARGA CELULAR - NAO PODE CANCELAR' confere_regra
        ,count(pedido) contagem_pedidos
        from `facily-817c2.facily_wp_logistic.log_pedidos_logistica` -- consulta no BQ
        where cast(pedido as string) in {pedidos}  
        and safe_cast(id_filial as INT64) in (118505359,118467542,118577682,118573777)
        """
        dados = self.client.query(query).result().to_dataframe(create_bqstorage_client=True).pedido.values
        dados_recarga_celular= np.array(list(map(str, dados)))
        #dados_n_dados_recarga_celular = np.setdiff1d(np.array(pedidos),dados_dados_recarga_celular)
        return list(dados_recarga_celular)





    def status_not_cancel(self, pedidos):
        query=f"""
        select pedido
        from `facily-817c2.facily_wp_logistic.log_pedidos_logistica` 
        where cast(pedido as string) in {pedidos} 
        and safe_cast(id_filial as INT64) in (97321472,97254276,71893174,70637894,73434034,68375042,69695432,69632218,65829734,66363252,72061147,66193890,85633500,121850703,76220405,53603282,110004908,68406778,
                                          71431645,72089320,66296625,94637473)
        """
        dados = self.client.query(query).result().to_dataframe(create_bqstorage_client=True).pedido.values
        dados_status_not_cancel= np.array(list(map(str, dados)))
        #dados_n_status_not_cancel = np.setdiff1d(np.array(pedidos),dados_status_not_cancel)
        return list(dados_status_not_cancel)




