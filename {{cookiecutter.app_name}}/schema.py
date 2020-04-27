from .schemas import MutationPet, QueryPet
import graphene


class PetsQuery(graphene.ObjectType):
    """
    Consultas das modelos dos app pets.
    """

    pets = graphene.Field(QueryPet, description="Queries relacionadas ao modelo pets")

    def resolve_pets(self, info, **kwargs):
        return info


class PetsMutation(graphene.ObjectType):
    """
    Mutação das modelos do app pets.
    """

    pets = graphene.Field(MutationPet, description="Mutações relacionadas ao modelo pets")

    def resolve_pets(self, info, **kwargs):
        return info
