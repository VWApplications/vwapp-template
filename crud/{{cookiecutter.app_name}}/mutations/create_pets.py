from common.scalars import DateField, PhoneField, PositiveIntegerField, PositiveFloatField
from common.utils import GenericUtils
from common.permissions import GenericPermissions
from petguard.pets.resolvers import CreatePetsResolver
from petguard.pets.types import PetType
from graphene.types import String, Boolean, Field
from graphene_file_upload.scalars import Upload
import graphene


class CreateAlimentationInput(graphene.InputObjectType):
    """
    Classe responsável pelos campos de criação da alimentação do pet.
    """

    qtd = String(required=True, description="Quantidade de ração diaria (SMALL, MEDIUM, BIG).")
    food = String(required=True, description="Nome da ração utilizada para alimentar o pet.")
    frequency = PositiveIntegerField(required=True, description="Quantidade de vezes que deve alimentar o animal por dia.")
    observations = String(required=False, description="Observações importantes.")


class CreateSpecialCaresInput(graphene.InputObjectType):
    """
    Classe responsável pelos campos de criação de cuidados especiais do pet.
    """

    veterinary_frequency = PositiveIntegerField(required=False, description="Quantidade de vezes que o animal vai ao veterinário por mês.")
    bathing_frequency = PositiveIntegerField(required=False, description="De quantos em quantos dias o animal toma banho.")
    diseases = String(required=False, description="Descrição sobre os problemas de saúde que o animal tem.")
    shear_type = String(required=False, description="Tipo de tosa.")
    shear_frequency = PositiveIntegerField(required=False, description="De quantos em quantos dias o animal é tosado.")
    deworming = String(required=False, description="Nome da última vermifugação tomada.")
    deworming_date = DateField(required=False, description="Data da última vermifugação.")
    vaccination = String(required=False, description="Nome da última vacinação tomada")
    vaccination_date = DateField(required=False, description="Data da última vacinação.")
    is_castrated = Boolean(required=False, description="O animal é castrado?")
    last_estro = DateField(required=False, description="Data do último CIO.")
    observations = String(required=False, description="Observações importantes.")
    veterinary_feedback = String(
        required=False,
        description="Feedbacks para uso veterinário caso alguém leve o pet para o veterinário e não tenha as informações necessárias."
    )


class CreatePetInput(graphene.InputObjectType):
    """
    Classe responsável pelos campos de criação do pet
    """

    name = String(required=True, description="Nome do animal de estimação.")
    kind = String(required=True, description="Tipo do animal de estimação (CAT, DOG).")
    sex = String(required=True, description="Sexo do animal de estimação (FEMALE, MALE).")
    height = String(required=True, description="Porte do animal de estimação (SMALL, MEDIUM, BIG).")
    temperament = String(required=True, description="Temperamento do animal de estimação (DOCILE, FRIENDLY, BRAVE).")
    age = PositiveIntegerField(required=False, description="Idade do animal de estimação.")
    breed = String(required=False, description="Raça do animal de estimação.")
    photo = Upload(required=False, description="Foto do animal de estimação.")
    phone = PhoneField(required=False, description="Telefone para contato caso encontre o dono.")
    weight = PositiveFloatField(required=False, description="Peso do animal de estimação.")
    description = String(required=False, description="Breve descrição do comportamento do animal ou outras informações.")

    alimentation = Field(
        CreateAlimentationInput,
        description="Dados relacionados a alimentação do pet.",
        required=False
    )

    special_cares = Field(
        CreateSpecialCaresInput,
        description="Dados relacionados a cuidados especiais do pet.",
        required=False
    )


class CreatePetMutation(graphene.Mutation):
    """
    Criar um pet.
    """

    pet = Field(
        PetType,
        description="Modelo de pet."
    )

    class Arguments:
        """
        Define os dados que você pode enviar para o servidor.
        """

        data = CreatePetInput(
            description="Corpo da requisição.",
            required=True
        )

    def mutate(self, info, data):
        """
        Mutações
        """

        logged_user = GenericUtils.get_logged_user(info)

        GenericPermissions.auth_validation(logged_user)

        pet = CreatePetsResolver(logged_user, data).get_result()

        return CreatePetMutation(pet=pet)
