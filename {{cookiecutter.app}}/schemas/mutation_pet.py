from petguard.pets.mutations import CreatePetMutation, UpdatePetMutation, DeletePetMutation
import graphene


class MutationPet(graphene.ObjectType):
    """
    Mutações da modelo pets.
    """

    create_pet = CreatePetMutation.Field()
    update_pet = UpdatePetMutation.Field()
    delete_pet = DeletePetMutation.Field()
