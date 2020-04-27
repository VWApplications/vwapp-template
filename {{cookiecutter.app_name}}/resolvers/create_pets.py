from common.validations import GenericValidations
from petguard.pets.models import Pet, Alimentation, SpecialCares
from petguard.pets.enum import (
    PetTypeEnum, PetSexEnum, PetSizeEnum,
    PetTemperamentEnum
)


class CreatePetsResolver:
    """
    Classe responsável pela lógica de criação de pets
    """

    def __init__(self, user, data):
        """
        Construtor
        """

        self.user, self.ong = Pet.objects.get_user_type(user)

        self.name = data.get('name')
        self.kind = data.get('kind')
        self.sex = data.get('sex')
        self.height = data.get('height')
        self.temperament = data.get('temperament')
        self.breed = data.get('breed', '')
        self.age = data.get('age', None)
        self.phone = data.get('phone', self.user.phone)
        self.photo = data.get('photo', None)
        self.weight = data.get('weight', 0.0)
        self.description = data.get('description', '')
        self.__get_alimentation_attributes(data)
        self.__get_special_cares_attributes(data)

    def __get_alimentation_attributes(self, data):
        """
        Pega os atributos relacionados a alimentação do pet.
        """

        self.alimentation = data.get('alimentation', None)

        if self.alimentation:
            self.qtd = self.alimentation.get('qtd')
            self.food = self.alimentation.get('food')
            self.frequency = self.alimentation.get('frequency')
            self.observations = self.alimentation.get('observations', '')

    def __get_special_cares_attributes(self, data):
        """
        Pega os atributos relacionados a cuidados especiais do pet.
        """

        self.special_cares = data.get('special_cares', None)

        if self.special_cares:
            self.veterinary_frequency = self.special_cares.get('veterinary_frequency', 0)
            self.bathing_frequency = self.special_cares.get('bathing_frequency', 0)
            self.diseases = self.special_cares.get('diseases', '')
            self.shear_type = self.special_cares.get('shear_type', '')
            self.shear_frequency = self.special_cares.get('shear_frequency', 0)
            self.veterinary_feedback = self.special_cares.get('veterinary_feedback', '')
            self.deworming = self.special_cares.get('deworming', '')
            self.deworming_date = self.special_cares.get('deworming_date', None)
            self.vaccination = self.special_cares.get('vaccination', '')
            self.vaccination_date = self.special_cares.get('vaccination_date', None)
            self.is_castrated = self.special_cares.get('is_castrated', False)
            self.last_estro = self.special_cares.get('last_estro', None)
            self.observations = self.special_cares.get('observations', '')

    def __validations(self):
        """
        Valida alguns dados de entrada.
        """

        GenericValidations.validate_required_field("name", self.name)
        GenericValidations.validate_required_field("kind", self.kind)
        GenericValidations.belongs_to_enum(PetTypeEnum, self.kind)
        GenericValidations.validate_required_field("sex", self.sex)
        GenericValidations.belongs_to_enum(PetSexEnum, self.sex)
        GenericValidations.validate_required_field("height", self.height)
        GenericValidations.belongs_to_enum(PetSizeEnum, self.height)
        GenericValidations.validate_required_field("temperament", self.temperament)
        GenericValidations.belongs_to_enum(PetTemperamentEnum, self.temperament)

        if self.alimentation:
            GenericValidations.validate_required_field("qtd", self.qtd)
            GenericValidations.belongs_to_enum(PetSizeEnum, self.qtd)
            GenericValidations.validate_required_field("food", self.food)
            GenericValidations.validate_required_field("frequency", self.frequency)

    def get_result(self):
        """
        Resultado do resolver.
        """

        self.__validations()

        pet = Pet(
            name=self.name,
            kind=self.kind,
            sex=self.sex,
            height=self.height,
            breed=self.breed,
            age=self.age,
            phone=self.phone,
            temperament=self.temperament,
            photo=self.photo,
            weight=self.weight,
            description=self.description
        )

        if self.ong:
            pet.ong = self.user
        else:
            pet.owner = self.user

        if self.alimentation:
            alimentation = Alimentation.objects.create(
                qtd=self.qtd,
                food=self.food,
                frequency=self.frequency,
                observations=self.observations
            )
            pet.alimentation = alimentation

        if self.special_cares:
            special_cases = SpecialCares.objects.create(
                veterinary_frequency=self.veterinary_frequency,
                bathing_frequency=self.bathing_frequency,
                diseases=self.diseases,
                shear_type=self.shear_type,
                shear_frequency=self.shear_frequency,
                veterinary_feedback=self.veterinary_feedback,
                deworming=self.deworming,
                deworming_date=self.deworming_date,
                vaccination=self.vaccination,
                vaccination_date=self.vaccination_date,
                is_castrated=self.is_castrated,
                last_estro=self.last_estro,
                observations=self.observations
            )
            pet.special_cares = special_cases

        pet.save()

        return pet
