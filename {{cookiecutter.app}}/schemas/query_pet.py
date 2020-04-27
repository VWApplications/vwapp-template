from petguard.pets.types import PetType
from petguard.pets.resolvers import ListPetResolver, FetchPetResolver
from graphene.types import String, Int, Boolean
import graphene


class QueryPet(graphene.ObjectType):
    """
    Tipo especial de consulta que obtem dados do servidor.
    """

    collection = graphene.List(
        PetType,
        description="Listar todos os pets de um usuário do pet guard.",
        identify=String(required=True, description="Identificador do usuário."),
        search=String(description="Procurar um pet pelo seu nome ou pelos dados da ong na qual ele pertence (nome, email ou cnpj)."),
        kind=String(description="Filtrar os pets do tipo DOG ou CAT."),
        is_adoption=Boolean(description="Filtra somente os pets que estão em adoção."),
        is_adopted=Boolean(description="Filtra por pets adotados."),
        skip=Int(description="Pula os primeiros N usuários."),
        first=Int(description="Pega os primeiros N usuários após o skip.")
    )

    instance = graphene.Field(
        PetType,
        description="Pegar os dados de um pet especifico do pet guard.",
        identify=String(required=True, description="Identificador do usuário."),
        pet_id=String(required=True, description="Identificador do pet.")
    )

    def resolve_collection(self, info, identify, **kwargs):
        """
        Cada campo é manipulado por meio de resolvers, que retornam um valor.
        """

        pets = ListPetResolver(identify, kwargs).get_result()

        return pets

    def resolve_instance(self, info, identify, pet_id):
        """
        Pega um usuário especifico
        """

        pet = FetchPetResolver(identify, pet_id).get_result()

        return pet
