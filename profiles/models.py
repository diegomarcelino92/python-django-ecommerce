from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError

from profiles.validators import cpf_validator


class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    document = models.CharField(max_length=30)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)

    def clean(self) -> None:
        errors = {}

        if not cpf_validator(self.document):
            errors['document'] = 'Invalid document'

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.user.get_username()


class ProfileAddress(models.Model):
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=50)
    code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    state = models.CharField(
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('PR', 'Paraná'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('RS', 'Rio Grande do Sul'),
            ('SC', 'Santa Catarina'),
            ('SE', 'Sergipe'),
            ('SP', 'São Paulo'),
            ('TO', 'Tocantins'),
        ))

    def __str__(self):
        return str(self.address)
