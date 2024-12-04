from django import forms
from tecnoApp.models import Equipamentos, Documentos, Usuario

class FormDocumento(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ('tipo_documento', 'tipo_contrato', 'servico', 'especificacoes', 'incluir_todos_equipamentos')


class FormEquipamento(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ('categoria', 'nome', 'especificacoes', 'foto')

        widgets = {
            'foto' : forms.FileInput(attrs={'accept': 'image/*'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        equipamento = super().save(commit=False)
        if self.user:
            equipamento.usuario = self.user
        if commit:
            equipamento.save()
        return equipamento


class FormLogin(forms.Form):
    tipo = forms.ChoiceField(
        choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')],
        widget=forms.HiddenInput(), 
        initial='PF'
    )
    cpf = forms.CharField(
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'CPF'})
    )
    cnpj = forms.CharField(
        max_length=18,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'CNPJ'})
    )
    senha = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cpf = cleaned_data.get('cpf')
        cnpj = cleaned_data.get('cnpj')

        if tipo == 'PF' and not cpf:
            raise forms.ValidationError('Informe o CPF para login.')
        if tipo == 'PJ' and not cnpj:
            raise forms.ValidationError('Informe o CNPJ para login.')

        return cleaned_data


class FormCriarLogin(forms.Form):
    nome = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nome'}), required=True)
    cpf = forms.CharField(max_length=14, required=False, widget=forms.TextInput(attrs={'placeholder': 'CPF'}))
    cnpj = forms.CharField(max_length=18, required=False, widget=forms.TextInput(attrs={'placeholder': 'CNPJ'}))
    senha = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
    tipo = forms.ChoiceField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], required=True)

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        cnpj = cleaned_data.get('cnpj')
        tipo = cleaned_data.get('tipo')

        # Validação de preenchimento correto
        if tipo == 'PF' and not cpf:
            raise forms.ValidationError('Informe o CPF para criar uma conta.')
        if tipo == 'PJ' and not cnpj:
            raise forms.ValidationError('Informe o CNPJ para criar uma conta.')

        if tipo == 'PF' and cnpj:
            raise forms.ValidationError('CNPJ não pode ser preenchido para Pessoa Física.')
        if tipo == 'PJ' and cpf:
            raise forms.ValidationError('CPF não pode ser preenchido para Pessoa Jurídica.')

        return cleaned_data

