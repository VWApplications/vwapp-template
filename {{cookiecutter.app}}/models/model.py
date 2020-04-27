from django.db import models
from common.exceptions import CustomError
from common.models import BaseModel
from petguard.users.models import PetGuardUser, PetGuardPartner
from .alimentation import Alimentation
from .special_cares import SpecialCares


class PetManager(models.Manager):
    """
    Gerenciado de querysets de pets.
    """

    def get_user_type(self, logged_user):
        """
        Pega o usuário normal ou usuário do tipo ONG a partir do usuário logado.
        """

        is_ong = False
        user = logged_user

        if hasattr(logged_user, "petguard_user"):
            user = PetGuardUser.objects.get_user(logged_user.email)
        elif hasattr(logged_user, "petguard_partner"):
            user = PetGuardPartner.objects.get_user(logged_user.email)
            is_ong = True
        else:
            raise CustomError(
                message="Usuário não tem conta no petguard.",
                cause=f"Usuário {user} não tem contan no petguard."
            )

        return user, is_ong

    def get_pet(self, identify, user):
        """
        Pega o pet pelo identificado passado e o usuário na qual pertence.
        """

        try:
            pet = Pet.objects.get(id=identify, owner=user)
        except Pet.DoesNotExist:
            raise CustomError(
                message="Não foi encontrado o pet com o identificador passado.",
                cause=f"ID: {identify}"
            )

        return pet

    def get_pet_ong(self, identify, ong):
        """
        Pega o pet pelo identificador passado e a ong na qual pertece.
        """

        try:
            pet = Pet.objects.get(id=identify, ong=ong)
        except Pet.DoesNotExist:
            raise CustomError(
                message="Não foi encontrado o pet com o identificador passado.",
                cause=f"ID: {identify}"
            )

        return pet

    def get_public_pet(self, identify):
        """
        Pega informações de um pet de forma pública.
        """

        try:
            pet = Pet.objects.get(id=identify)
        except Pet.DoesNotExist:
            raise CustomError(
                message="Não foi encontrado o pet com o identificador passado.",
                cause=f"ID: {identify}"
            )

        return pet


class Pet(BaseModel):
    """
    Animal de estimação.
    """

    owner = models.ForeignKey(
        PetGuardUser,
        on_delete=models.PROTECT,
        help_text="Dono do pet ou usuário que adotou o pet.",
        related_name='pets',
        null=True
    )

    ong = models.ForeignKey(
        PetGuardPartner,
        on_delete=models.PROTECT,
        help_text="ONG responsável pelo pet.",
        related_name='pets',
        null=True
    )

    alimentation = models.OneToOneField(
        Alimentation,
        on_delete=models.CASCADE,
        help_text="Alimentação do pet.",
        related_name='pet',
        null=True
    )

    special_cares = models.OneToOneField(
        SpecialCares,
        on_delete=models.CASCADE,
        help_text="Cuidados do pet.",
        related_name='pet',
        null=True
    )

    name = models.CharField(
        "Nome do pet",
        help_text="Nome do animal de estimação.",
        max_length=30
    )

    breed = models.CharField(
        "Raça do pet",
        help_text="Raça do animal de estimação.",
        max_length=20,
        blank=True
    )

    kind = models.CharField(
        "Tipo de pet.",
        help_text="Tipo do animal de estimação (CAT, DOG).",
        max_length=11
    )

    sex = models.CharField(
        "Sexo de pet.",
        help_text="Sexo do animal de estimação (FEMALE, MALE).",
        max_length=11
    )

    age = models.PositiveIntegerField(
        "Idade do pet.",
        help_text="Idade do animal de estimação.",
        null=True
    )

    phone = models.CharField(
        "Telefone para contato.",
        help_text="Telefone para contato caso encontre o dono.",
        max_length=11,
        blank=True
    )

    height = models.CharField(
        "Porte do pet.",
        help_text="Porte do animal de estimação (SMALL, MEDIUM, BIG).",
        max_length=11
    )

    temperament = models.CharField(
        "Temperamento do pet.",
        help_text="Temperamento do animal de estimação (DOCILE, FRIENDLY, BRAVE).",
        max_length=20
    )

    photo = models.ImageField(
        upload_to="petguard_pets",
        help_text="Foto do animal de estimação.",
        verbose_name="Foto",
        blank=True, null=True
    )

    weight = models.FloatField(
        "Peso do pet",
        help_text="Peso do animal de estimação.",
        null=True
    )

    description = models.TextField(
        "Descrição do animal",
        help_text="Breve descrição do comportamento do animal ou outras informações.",
        blank=True
    )

    is_adopted = models.BooleanField(
        "O pet foi adotado?",
        help_text="Verifica se o pet foi adotado por uma ong parceira.",
        default=False
    )

    objects = PetManager()

    def __str__(self):
        """
        Retorno o objeto em formato de string.
        """

        return self.name

    class Meta:
        """
        Algumas informações adicionais.
        """

        db_table = "petguard_pets"
        ordering = ('created_at',)
