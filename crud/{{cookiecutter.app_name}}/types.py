from graphene_django import DjangoObjectType
from common.generic_types import FileType
from .models import Pet, Alimentation, SpecialCares
import graphene


class AlimentationType(DjangoObjectType):
    """
    Objeto com todos os campos da modelo Alimentation.
    """

    class Meta:
        model = Alimentation
        fields = ('qtd', 'food', 'frequency', 'observations')


class SpecialCaresType(DjangoObjectType):
    """
    Objeto com todos os campos da modelo SpecialCares.
    """

    class Meta:
        model = SpecialCares
        fields = (
            'veterinary_frequency', 'bathing_frequency', 'diseases',
            'shear_type', 'shear_frequency', 'veterinary_feedback',
            'deworming', 'deworming_date', 'vaccination', 'vaccination_date',
            'is_castrated', 'last_estro', 'observations'
        )


class PetType(DjangoObjectType):
    """
    Objeto com todos os campos da modelo Pet.
    """

    class Meta:
        model = Pet
        fields = (
            'id', 'name', 'breed', 'kind', 'sex', 'age',
            'phone', 'height', 'temperament', 'photo',
            'alimentation', 'special_cares', 'owner',
            'weight', 'description'
        )

    photo = graphene.Field(
        FileType,
        description="Foto do pet."
    )

    @staticmethod
    def resolve_photo(parent, info):
        """
        Pega a foto do pet.
        """

        if parent is not None:
            if parent.photo:
                return parent.photo

        return {
            "url": '',
            "name": '',
            "size": 0,
            "width": 0
        }
