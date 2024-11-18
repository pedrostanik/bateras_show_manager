from django import forms
from django.forms import inlineformset_factory
from .models import Banda, Evento, Musico

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['data', 'local', 'aberto']  # Campos do formulário

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}), 
            'local': forms.TextInput(attrs={'maxlength': 100, 'placeholder': 'Local do evento'}),
            'aberto': forms.CheckboxInput(), 
            "class": "form-control", 
        }

class BandaForm(forms.ModelForm):
    class Meta:
        model = Banda
        fields = ['evento', 'nome_banda']

class MusicoForm(forms.ModelForm):

    class Meta:
        model = Musico
        fields = ['nome_musico', 'cpf_musico', 'papel']
        widgets = {
            'papel': forms.Select(choices=Musico.ROLE_CHOICES),
        }

MusicoFormSet = inlineformset_factory(Banda, Musico, form=MusicoForm, extra=0, can_delete=True)



# class EventoForm(forms.Form):
    # data = forms.DateField(
    #     label="Data do Evento",
    #     required=True,
    #     input_formats=['%Y-%m-%d'],
    #     widget=forms.DateInput(
    #         attrs={
    #             "type": 'date'
    #         }
    #     )
    # )

    # local = forms.CharField(
    #     label="Local do Evento",
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Digite aqui o nome do local"  
    #         }
    #     )
    # )
    
    # aberto = forms.BooleanField(
    #     label="Aberto",
    # )