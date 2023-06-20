from django.shortcuts import render
from django.http import HttpResponse
from .models import Pessoa

def ver_produto(request):
    if request.method == "GET":
        nome = 'Gugu'
        idade = 2222222
        return render(request, 'ver_produto.html', {'nome': nome, 'idade': idade})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        
        #Formulario irá adicionar um usuario:
        '''pessoa = Pessoa(nome=nome, idade=idade)
        
        pessoa.save()'''
        
        #Formulario irá mostrar todos usuarios registrados:
        '''pessoas = Pessoa.objects.all()
        print(pessoas)'''
        
        #Formulario irá filtrar de acordo com a variavel usada e mostrar o usuario apenas se ele for igual a variavel:
        pessoas = Pessoa.objects.filter(nome=nome)
        print(pessoas)
        
        #Verifica se o usuario ja existe
        if Pessoa.exists():
            print('Usuario ja existe.')
        else:
            print('Usuario cadastrado com sucesso.')
        
        return HttpResponse(pessoas)


def inserir_produto(request):
    return HttpResponse('Inserir')
