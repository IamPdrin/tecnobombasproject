from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader

from tecnoApp.models import Documentos, Equipamentos, Usuario
from tecnoApp.forms import FormEquipamento, FormDocumento, FormLogin, FormCriarLogin
from django.contrib import messages

def landing_page(request):
    return render(request, 'landingPage.html')

def sel_documento(request):
    return render(request, 'sel_documento.html')

def fazerLogin(request):
    formLogin = FormLogin(request.POST or None)
    
    if request.method == 'POST':
        if formLogin.is_valid():
            
            cnpj = formLogin.cleaned_data.get('cnpj')
            cpf = formLogin.cleaned_data.get('cpf')
            senha = formLogin.cleaned_data.get('senha')

            try:
                if cpf:
                    user = Usuario.objects.get(cpf=cpf)
                elif cnpj:
                    user = Usuario.objects.get(cnpj=cnpj)
                else:
                    raise Usuario.DoesNotExist

                if user.senha == senha:
                    return redirect('principal')  
                else:
                    messages.error(request, "Senha incorreta.") 
            except Usuario.DoesNotExist:
                messages.error(request, "Credenciais inválidas.") 

    context = {'formLogin': formLogin}
    return render(request, 'login.html', context)


def criarLogin(request):
    formCriarLogin = FormCriarLogin(request.POST or None)

    if request.method == 'POST':
        if formCriarLogin.is_valid():
            nome = formCriarLogin.cleaned_data.get('nome')
            cpf = formCriarLogin.cleaned_data.get('cpf') or None
            cnpj = formCriarLogin.cleaned_data.get('cnpj') or None
            senha = formCriarLogin.cleaned_data.get('senha')

            # Determinar o tipo com base nos dados preenchidos
            tipo = 'PF' if cpf else 'PJ'

            # Verificar duplicidade
            if cpf and Usuario.objects.filter(cpf=cpf).exists():
                messages.error(request, "CPF já cadastrado.")
            elif cnpj and Usuario.objects.filter(cnpj=cnpj).exists():
                messages.error(request, "CNPJ já cadastrado.")
            else:
                # Criar usuário com o tipo correto
                Usuario.objects.create(nome=nome, cpf=cpf, cnpj=cnpj, senha=senha, tipo=tipo)
                messages.success(request, "Usuário criado com sucesso!")
                return redirect('fazerLogin')

    context = {'formCriarLogin': formCriarLogin}
    return render(request, 'criar_login.html', context)


def principal(request):
    equipList = Equipamentos.objects.all()
    docList = Documentos.objects.all()
    context = {
        'equipamentos': equipList,
        'documentos': docList,
    }

    template = loader.get_template('principal.html')

    return HttpResponse(template.render(context))


def excluir_equipamento(request, id_equipamento):
    equipamento = Equipamentos.objects.get(id=id_equipamento)
    equipamento.delete()

    return redirect('principal')

def excluir_documento(request, id_documento):
    documento = Documentos.objects.get(id=id_documento)
    documento.delete()

    return redirect('principal')


def add_equipamento(request):
    formEquipamento = FormEquipamento(request.POST or None, request.FILES or None)

    if formEquipamento.is_valid():
        equipamento = formEquipamento.save(commit=False)


        if request.user.is_authenticated:
            equipamento.usuario = request.user
        else:
            equipamento.usuario = None
        
        equipamento.save() 
        messages.success(request, "Equipamento cadastrado com sucesso!")
        return redirect('principal')
    
    context = {
        'form' : formEquipamento
    }

    return render(request, 'add_equipamento.html', context)


def add_proposta(request):
    formProposta = FormDocumento(request.POST or None)

    if formProposta.is_valid():
        formProposta.save()

        return redirect('sel_documento')
    
    context = {
        'formProposta' : formProposta
    }

    return render(request, 'add_proposta.html', context)


def add_orcamento(request):
    formOrcamento = FormDocumento(request.POST or None)

    if formOrcamento.is_valid():
        formOrcamento.save()

        return redirect('sel_documento')
    
    context = {
        'formOrcamento' : formOrcamento
    }

    return render(request, 'add_orcamento.html', context)


def add_outros(request):
    formOutro = FormDocumento(request.POST or None)

    if formOutro.is_valid():
        formOutro.save()

        return redirect('sel_documento')
    
    context = {
        'formOutro' : formOutro
    }

    return render(request, 'add_outro.html', context)


def edt_equipamento(request, id_equipamento):
    equipamento = Equipamentos.objects.get(id=id_equipamento)

    formEdt = FormEquipamento(request.POST or None, instance=equipamento)
    if request.POST:
        if formEdt.is_valid():
            formEdt.save()
            return redirect('principal')
        
    context = {
        'form' : formEdt
    }
    return render(request, 'edt_equipamento.html', context)


def edt_documento(request, id_documento):
    documento = Documentos.objects.get(id=id_documento)

    formEdtDoc = FormDocumento(request.POST or None, instance=documento)
    if request.POST:
        if formEdtDoc.is_valid():
            formEdtDoc.save()
            return redirect('principal')
        
    context = {
        'form' : formEdtDoc
    }
    return render(request, 'edt_documento.html', context)



