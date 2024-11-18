from django.db import models

class Evento(models.Model):
    data = models.DateField()
    local = models.CharField(max_length=100)
    aberto = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.data} - {self.local}'

class Banda(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE) 
    nome_banda = models.CharField(max_length=100)
    nome_musico = models.CharField(max_length=100)
    cpf_musico = models.CharField(max_length=20)
    papel = models.CharField(max_length=50, help_text="Função ou papel do aluno na banda")    
    
    def __str__(self):
        return f'{self.evento} - {self.cpf_musico} - {self.nome_musico} - {self.papel} na banda {self.nome_banda}'
    
class Musico(models.Model):
    ROLE_CHOICES = [
        ('Vocalista', 'Vocalista'),
        ('Guitarrista', 'Guitarrista'),
        ('Baterista', 'Baterista'),
        ('Baixista', 'Baixista'),
        ('Tecladista', 'Tecladista'),
        
        # Adicione mais opções aqui conforme necessário
    ]
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name='integrantes')
    nome_musico = models.CharField(max_length=100)
    cpf_musico = models.CharField(max_length=20)
    papel = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.cpf_musico} - {self.nome_musico} - {self.papel} na banda {self.banda}'
    

