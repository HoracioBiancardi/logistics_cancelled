from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from pyparsing import quoted_string
from tablib import Dataset

from accounts.resources import PedidosCancelamentosResource

from .models import PedidosCancelamento
from .regras import RegrasCancelamento


def login(request):
    if request.method !='POST':
        return render(request, 'accounts/login.html')
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, "Usuario ou senha inválidos")
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, "Login efetuado com sucesso ")
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    messages.success(request, "Logout efetuado com sucesso ")
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    qtd_pedidos_dia =PedidosCancelamento.objects.extra(
        select={'day': 'date( data_inclusao )'}).values('day')\
            .annotate(
                pedido=Count('id_pedido'), 
                cancelamento=Q(env_cancelamento=True))
    
    #print([ x['pedido'] for x in list(qtd_pedidos_dia) ])

    #chart = {'dados':{'day':[qtd_pedidos_dia]

# [{'day': '2022-02-10', 'pedido': 2, 'cancelamento': False}, 
# {'day': '2022-02-09', 'pedido': 1, 'cancelamento': True}, 
# {'day': '2022-02-10', 'pedido': 14, 'cancelamento': True}]


    dados = {
        'data_can':[x['day'] for x in list(qtd_pedidos_dia) if x['cancelamento']],
        'pedido_can':[x['pedido']for x in list(qtd_pedidos_dia) if x['cancelamento']],
        'data_n_can':[x['day'] for x in list(qtd_pedidos_dia) if x['cancelamento'] is False],
        'pedido_n_can':[x['pedido']for x in list(qtd_pedidos_dia) if x['cancelamento'] is False],

    }



    return render(request, 'accounts/dashboard.html', dados)









@login_required(redirect_field_name='login')
def importCSV(request):
    if request.method == 'POST' and 'myfile' in request.FILES:
        regras = RegrasCancelamento()

        pedidos_cancelamento_resource = PedidosCancelamentosResource()
        dataset=Dataset()
        doc = request.FILES 
        new_cancelamento = doc['myfile']

        new_motivo = request.POST.get('motivo')
        if not new_motivo:
            messages.error(request, 'O campo não pode estar vazio.')
            return render(request, 'accounts/importCSV.html')


        if not new_cancelamento.name.endswith('csv'):
            messages.error(request, "Envie o arquivo no formato CSV.")
            return render(request, 'accounts/importCSV.html')
       
        result = pedidos_cancelamento_resource.import_data(dataset, dry_run=True)
        imported_data=dataset.load(new_cancelamento.read().decode(), format='csv', headers=False)
        
        count_row_exp=len(imported_data) 
        count_row_db_old = PedidosCancelamento.objects.count()

        if not result.has_errors():
            resul_cancel = regras.env_cancelamento(tuple(imported_data.export('df')[0].tolist()))
            resul_cross = regras.cross_border(tuple(imported_data.export('df')[0].tolist()))
            resul_recarga_cel = regras.cross_border(tuple(imported_data.export('df')[0].tolist()))
            resul_cash = regras.cash(tuple(imported_data.export('df')[0].tolist()))
            resul_status_not_cancel = regras.status_not_cancel(tuple(imported_data.export('df')[0].tolist()))




            
            for data in imported_data.export('df')[0].tolist():
                try:
                    obj = PedidosCancelamento.objects.get(id_pedido=data)
                except PedidosCancelamento.DoesNotExist:                   
                    obj = PedidosCancelamento(
                        id_pedido=data, 
                        nome_user=request.user.username,
                        motivo=new_motivo,
                        )
                    obj.save()
                        
            if resul_cancel:
                for x in resul_cancel:
                    obj = PedidosCancelamento.objects.get(id_pedido=x)
                    obj.env_cancelamento=True
                    obj.save()
            if resul_cross:
                for x in resul_cross:
                    obj = PedidosCancelamento.objects.get(id_pedido=x)
                    obj.corss_border=True
                    obj.save()
            if resul_recarga_cel:
                for x in resul_recarga_cel:
                    obj = PedidosCancelamento.objects.get(id_pedido=x)
                    obj.recarga_celular=True
                    obj.save()
            if resul_cash:
                for x in resul_cash:
                    obj = PedidosCancelamento.objects.get(id_pedido=x)
                    obj.cash=True
                    obj.save()
            if resul_status_not_cancel:
                for x in resul_status_not_cancel:
                    obj = PedidosCancelamento.objects.get(id_pedido=x)
                    obj.status_not_cancel=True
                    obj.save()


        count_row_db_dep = PedidosCancelamento.objects.count() 

        if count_row_db_dep <= count_row_db_old:
            messages.error(request, f"Não foi enviado nenhum pedido pois os mesmos ja estão na base de dados")
            return redirect('dashboard')
        else:
            messages.info(request, f"Exportado {count_row_exp} pedidos do arquivo, foi enviado para a base {count_row_db_dep-count_row_db_old}.")
            messages.info(request, f"Envido para cancelamento pelo motivo: {new_motivo}")
            return redirect('dashboard')
                
    return render(request, 'accounts/importCSV.html')




# @login_required(redirect_field_name='login')
# def chart_data(request):
#     resp = StreamingHttpResponse(stream_response_generator(), content_type='text/event-stream')
#     return resp

# def stream_response_generator():
#     obj = PedidosCancelamento.objects.count()
#     json_data = json.dumps(
#         {'time': datetime.now().strftime('%H:%M:%S'), 'value': obj}) 
#     yield f"data:{json_data}\n\n"




