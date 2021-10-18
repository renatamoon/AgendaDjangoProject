from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

# Create your views here.

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuario ou senha inválidos!')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login realizado com sucesso!')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('dashboard') #deslogando o user e mandando para a dashboard

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha2:
        messages.error(request, 'Os campos não podem permanecer vazios')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-MAIL INVÁLIDO')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'A SENHA PRECISA TER 6 CARACTERES')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.error(request, 'O USUÁRIO PRECISA TER 6 CARACTERES OU MAIS')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.error(request, 'AS SENHAS INFORMADAS NÃO CONFEREM')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'O USUÁRIO NÃO EXISTE!')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'O E-MAIL JÁ EXISTE!')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'REGISTRADO COM SUCESSO! Agora faça o login!')

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login') #nao pode ser acessada caso não estiver logado
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form}) #enviando um
    #formulario para a dashboard
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid:
        messages.error(request, 'ERRO AO ENVIAR O FORMULÁRIO')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'DESCRIÇÃO PRECISA TER MAIS QUE 5 CARACTERES!')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'O contato {request.POST.get("nome")} foi salvo com sucesso')
    return redirect('dashboard')



