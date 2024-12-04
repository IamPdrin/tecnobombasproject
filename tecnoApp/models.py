from django.db import models
from django.core.exceptions import ValidationError

class Endereco(models.Model):
    cep = models.CharField(max_length=10)  # Formato: 00000-000
    numero = models.CharField(max_length=10)  # Exemplo: "123A"
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # Exemplo: "SP"

    def __str__(self):
        return f"{self.numero}, {self.cep}, {self.cidade}-{self.estado}"

class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]

    senha = models.CharField(max_length=16)

    nome = models.CharField(max_length=255)
    tipo = models.CharField(
        max_length=2,
        choices=TIPO_USUARIO_CHOICES,
        default='PF',
    )
    cpf = models.CharField(
        max_length=14,  # Formato: 000.000.000-00
        blank=True,
        null=True,
        unique=True,
    )
    cnpj = models.CharField(
        max_length=18,  # Formato: 00.000.000/0000-00
        blank=True,
        null=True,
        unique=True,
    )
    endereco = models.OneToOneField(
        Endereco,
        on_delete=models.CASCADE,
        related_name="usuario",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        # Validações de consistência de tipo e documentos
        if self.tipo == 'PF' and not self.cpf:
            raise ValueError("Usuários do tipo PF devem ter um CPF.")
        if self.tipo == 'PJ' and not self.cnpj:
            raise ValueError("Usuários do tipo PJ devem ter um CNPJ.")
        if self.tipo == 'PF' and self.cnpj:
            raise ValueError("Usuários do tipo PF não devem ter um CNPJ.")
        if self.tipo == 'PJ' and self.cpf:
            raise ValueError("Usuários do tipo PJ não devem ter um CPF.")


        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({'PF' if self.tipo == 'PF' else 'PJ'})"
    

class Equipamentos(models.Model):
    #categoria, nome, especificacoes, img
    categoria = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    especificacoes = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='images/', null=True, blank=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='equipamentos',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nome


class Documentos(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('Orçamento', 'Orçamento'),
        ('Proposta de Contrato', 'Proposta de Contrato'),
        ('Outros', 'Outros'),
    ]

    TIPO_CONTRATO_CHOICES = [
        ('Manutenção Hidráulica Taxa Zero', 'Manutenção Hidráulica Taxa Zero'),
        ('Manutenção Hidráulica Comum', 'Manutenção Hidráulica Comum'),
        ('Tratamento Químico da Piscina', 'Tratamento Químico da Piscina'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='documentos',
    )

    equipamentos = models.ManyToManyField(
        Equipamentos,
        related_name='documentos',
    )

    tipo_documento = models.CharField(
        max_length=50,
        choices=TIPO_DOCUMENTO_CHOICES,
    )

    tipo_contrato = models.CharField(
        max_length=50,
        choices=TIPO_CONTRATO_CHOICES,
        blank=True,
        null=True,
    )

    servico = models.TextField(
        blank=True,
        null=True,
        help_text="Detalhes do orçamento (apenas para tipo 'Orçamento')."
    )

    especificacoes = models.TextField(
        blank=True,
        null=True,
        help_text="Informações adicionais (apenas para tipo 'Outros')."
    )

    incluir_todos_equipamentos = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Validação lógica
        if self.tipo_documento == 'Proposta de Contrato' and not self.tipo_contrato:
            raise ValidationError("O campo 'tipo_contrato' é obrigatório para documentos do tipo 'Proposta de Contrato'.")
        if self.tipo_documento == 'Orçamento' and not self.servico:
            raise ValidationError("O campo 'servico' é obrigatório para documentos do tipo 'Orçamento'.")
        if self.tipo_documento == 'Outros' and not self.especificacoes:
            raise ValidationError("O campo 'especificacoes' é obrigatório para documentos do tipo 'Outros'.")

        # Garante que campos irrelevantes fiquem nulos
        if self.tipo_documento != 'Proposta de Contrato':
            self.tipo_contrato = None
        if self.tipo_documento != 'Orçamento':
            self.servico = None
        if self.tipo_documento != 'Outros':
            self.especificacoes = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_documento} - {self.usuario.nome}"
