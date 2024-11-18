from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from bands.models import Evento, Banda, Musico
from django.contrib import messages
from django.forms import modelformset_factory
from django.db.models import Count
from bands.forms import EventoForm, BandaForm, MusicoFormSet
from django.http import JsonResponse
import json


def home(request):
    return render(request, 'bands/home.html')

def eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'bands/eventos.html', {'eventos': eventos})

def bandas(request):
    bandas = Banda.objects.all()
    musicos = Musico.objects.all()
    bandas_list = []
    for banda in bandas:
        bandas_dict = {}
        bandas_dict['banda'] = banda.nome_banda
        bandas_dict['id'] = banda.id
        
        integrantes_list = []
        for musico in musicos:
            musicos_dict = {}
            if musico.banda_id == banda.id:
                musicos_dict['nome'] = musico.nome_musico
                musicos_dict['cpf'] = musico.cpf_musico
                musicos_dict['papel'] = musico.papel
                integrantes_list.append(musicos_dict)

        bandas_dict['integrantes'] = integrantes_list        
        bandas_list.append(bandas_dict)

    print(f'bandas_list: {bandas_list}')
    return render(request, 'bands/bandas.html', {
        'bandas': bandas_list,
        })

def evento_form(request):
    form = EventoForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        form.save()  
        return redirect('eventos')
    else:
        form = EventoForm()

    return render(request, 'bands/evento_form.html', {'form': form})

@transaction.atomic
def edit_banda(request, banda_id):
    # banda = Banda.objects.get(pk=banda_id) 
    banda = get_object_or_404(Banda, pk=banda_id) 
    integrantes = Musico.objects.filter(banda=banda_id) 

    if request.method == 'POST':
        print(f'request POST: {request.POST}')
        banda_form = BandaForm(request.POST, instance=banda)

        # Editando o formset com dados iniciais dos integrantes
        MusicoFormSet = modelformset_factory(Musico, fields=('nome_musico', 'cpf_musico', 'papel'), extra=0, can_delete=True)
        print(f'MusicoFormSet: {MusicoFormSet}')
        musico_formset = MusicoFormSet(request.POST, queryset=integrantes, prefix='form')

        # Verifica se o formulário e o formset são válidos
        print(f'verificando form válido...')
        # print(f'musico_formset: {musico_formset}')
        if banda_form.is_valid() and musico_formset.is_valid():    
            banda = banda_form.save()  # Salva a banda

            # Atualiza cada integrante
            for form in musico_formset:
                if form.is_valid():
                    print(f'form: {form.cleaned_data}')
                    if form.cleaned_data.get('DELETE'):
                        print('DELEEEEEEEEEEEETING!')
                        # Se o campo DELETE for True, exclua o músico
                        musico_instance = form.instance  # Obtém a instância do músico
                        musico_instance.delete()  # Exclui o músico
                        print(f'Músico {musico_instance.nome_musico} deletado!')
                    else:
                        musico_instance = form.save(commit=False)  # Não salva ainda
                        musico_instance.banda = banda  # Atribui a banda
                        musico_instance.save()  # Salva o músico
            return redirect('bandas')

    if banda_id:
        banda_form = BandaForm(initial={'evento':  banda.evento, 'nome_banda': banda.nome_banda})
        # Criando o formset com dados iniciais dos integrantes
        MusicoFormSet = modelformset_factory(Musico, fields=('nome_musico', 'cpf_musico', 'papel'), extra=0)
        musico_formset = MusicoFormSet(queryset=integrantes, prefix='form')
        
        return render(request, 'bands/register_banda.html', {
        'banda_form': banda_form,
        'musico_formset': musico_formset,
        'edit': True,
        'banda': banda
    })


@transaction.atomic
def register_banda(request):
    print('hello, you!')
    if request.method == 'POST':
        print(f'request.POST: {request.POST}')
        banda_form = BandaForm(request.POST)
        musico_formset = MusicoFormSet(request.POST, prefix='form')  
        print(f'musico_formset: {musico_formset}')

        if banda_form.is_valid() and musico_formset.is_valid():
            banda = banda_form.save() 
            for form in musico_formset:
                if form.is_valid():
                    form.instance.banda = banda
                    form.save()

            return redirect('bandas')  
        else:
            print(f'Erro: {musico_formset.errors}')  
            messages.error(request, 'Falha ao registrar banda!')
            return render(request, 'bands/register_banda.html', {
            'banda_form': banda_form,
            'musico_formset': musico_formset,
    })
    else:
        banda_form = BandaForm()
        musico_formset = MusicoFormSet(prefix='form')

    return render(request, 'bands/register_banda.html', {
        'banda_form': banda_form,
        'musico_formset': musico_formset,
    })

def cancelar_registro_banda(request):
    return redirect('bandas')

def get_students(request):
    max_number = int(request.GET.get('max_number', 0))
    musicos = (
        Musico.objects
        .values('nome_musico')
        .annotate(nome_count=Count('nome_musico'))
        .filter(nome_count__gt=max_number)
    )
    print(f'musicos: {musicos}')
        # Converte o QuerySet para uma lista de dicionários
    musicos_list = list(musicos)  # Cada item já é um dicionário com os campos `nome_musico` e `nome_count`

    return JsonResponse(musicos_list, safe=False)