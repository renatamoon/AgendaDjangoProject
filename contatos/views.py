from django.shortcuts import render, get_object_or_404, redirect
from . models import Contato
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contatos = Contato.objects.all()
    paginator = Paginator(contatos, 6)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html',{
        'contatos': contatos
    })

def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404()
    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })

#pega
def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR,
        'O campo não pode ficar vazio' )
        return redirect('index')

    campos = Concat('nome', Value(' '), 'sobrenome')
                            #o campo Value simula um campo que existe na minha base de dados
                            #filtrar por um termo - no caso Nome ou Sobrenome
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo) #coloco o iconts
        #para também mostrar os campos do telefone
    )
    paginator = Paginator(contatos, 3)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })