from common.validations import GenericValidations
from petguard.pets.models import Pet
from petguard.pets.enum import (
    PetTypeEnum, PetSexEnum, PetSizeEnum,
    PetTemperamentEnum
)


class UpdatePetsResolver:
    """
    Classe responsável pela lógica de atualização de pets
    """

    def __init__(self, user, identify, data):
        """
        Construtor
        """

        self.user, ong = Pet.objects.get_user_type(user)

        if ong:
            self.pet = Pet.objects.get_pet_ong(identify, self.user)
        else:
            self.pet = Pet.objects.get_pet(identify, self.user)

        self.pet.name = data.get('name', self.pet.name)
        self.pet.kind = data.get('kind', self.pet.kind)
        self.pet.sex = data.get('sex', self.pet.sex)
        self.pet.height = data.get('height', self.pet.height)
        self.pet.temperament = data.get('temperament', self.pet.temperament)
        self.pet.breed = data.get('breed', self.pet.breed)
        self.pet.age = data.get('age', self.pet.age)
        self.pet.phone = data.get('phone', self.pet.phone)
        self.pet.photo = data.get('photo', self.pet.photo)
        self.pet.weight = data.get('weight', self.pet.weight)
        self.pet.description = data.get('description', self.pet.description)
        self.__get_alimentation_attributes(data)
        self.__get_special_cares_attributes(data)

    def __get_alimentation_attributes(self, data):
        """
        Pega os atributos relacionados a alimentação do pet.
        """

        self.alimentation = data.get('alimentation', None)

        if self.alimentation:
            self.pet.alimentation.qtd = self.alimentation.get(
                'qtd',
                self.pet.alimentation.qtd if self.pet.alimentation else None
            )

            self.pet.alimentation.food = self.alimentation.get(
                'food',
                self.pet.alimentation.food if self.pet.alimentation else None
            )

            self.pet.alimentation.frequency = self.alimentation.get(
                'frequency',
                self.pet.alimentation.frequency if self.pet.alimentation else None
            )

            self.pet.alimentation.observations = self.alimentation.get(
                'observations',
                self.pet.alimentation.observations if self.pet.alimentation else ''
            )

    def __get_special_cares_attributes(self, data):
        """
        Pega os atributos relacionados a cuidados especiais do pet.
        """

        self.special_cares = data.get('special_cares', None)

        if self.special_cares:
            self.pet.special_cares.veterinary_frequency = self.special_cares.get(
                'veterinary_frequency',
                self.pet.special_cares.veterinary_feedback if self.pet.special_cares else 0
            )

            self.pet.special_cares.bathing_frequency = self.special_cares.get(
                'bathing_frequency',
                self.pet.special_cares.bathing_frequency if self.pet.special_cares else 0
            )

            self.pet.special_cares.diseases = self.special_cares.get(
                'diseases',
                self.pet.special_cares.diseases if self.pet.special_cares else ''
            )

            self.pet.special_cares.shear_type = self.special_cares.get(
                'shear_type',
                self.pet.special_cares.shear_type if self.pet.special_cares else ''
            )

            self.pet.special_cares.shear_frequency = self.special_cares.get(
                'shear_frequency',
                self.pet.special_cares.shear_frequency if self.pet.special_cares else 0
            )

            self.pet.special_cares.veterinary_feedback = self.special_cares.get(
                'veterinary_feedback',
                self.pet.special_cares.veterinary_feedback if self.pet.special_cares else ''
            )

            self.pet.special_cares.deworming = self.special_cares.get(
                'deworming',
                self.pet.special_cares.deworming if self.pet.special_cares else ''
            )

            self.pet.special_cares.deworming_date = self.special_cares.get(
                'deworming_date',
                self.pet.special_cares.deworming_date if self.pet.special_cares else None
            )

            self.pet.special_cares.vaccination = self.special_cares.get(
                'vaccination',
                self.pet.special_cares.vaccination if self.pet.special_cares else ''
            )

            self.pet.special_cares.vaccination_date = self.special_cares.get(
                'vaccination_date',
                self.pet.special_cares.vaccination_date if self.pet.special_cares else None
            )

            self.pet.special_cares.is_castrated = self.special_cares.get(
                'is_castrated',
                self.pet.special_cares.is_castrated if self.pet.special_cares else False
            )

            self.pet.special_cares.last_estro = self.special_cares.get(
                'last_estro',
                self.pet.special_cares.last_estro if self.pet.special_cares else None
            )

            self.pet.special_cares.observations = self.special_cares.get(
                'observations',
                self.pet.special_cares.observations if self.pet.special_cares else ''
            )

    def __validations(self):
        """
        Valida alguns dados de entrada.
        """

        GenericValidations.validate_required_field("name", self.pet.name)
        GenericValidations.validate_required_field("kind", self.pet.kind)
        GenericValidations.belongs_to_enum(PetTypeEnum, self.pet.kind)
        GenericValidations.validate_required_field("sex", self.pet.sex)
        GenericValidations.belongs_to_enum(PetSexEnum, self.pet.sex)
        GenericValidations.validate_required_field("height", self.pet.height)
        GenericValidations.belongs_to_enum(PetSizeEnum, self.pet.height)
        GenericValidations.validate_required_field("temperament", self.pet.temperament)
        GenericValidations.belongs_to_enum(PetTemperamentEnum, self.pet.temperament)

        if self.pet.alimentation:
            GenericValidations.validate_required_field("qtd", self.pet.alimentation.qtd)
            GenericValidations.belongs_to_enum(PetSizeEnum, self.pet.alimentation.qtd)
            GenericValidations.validate_required_field("food", self.pet.alimentation.food)
            GenericValidations.validate_required_field("frequency", self.pet.alimentation.frequency)

    def get_result(self):
        """
        Resultado do resolver.
        """

        self.__validations()

        self.pet.alimentation.save()
        self.pet.special_cares.save()
        self.pet.save()

        return self.pet
