from common.utils import GenericUtils
from common.permissions import GenericPermissions
from petguard.pets.resolvers import DeletePetsResolver
from graphene.types import Int, Boolean
import graphene


class DeletePetMutation(graphene.Mutation):
    """
    deletar um pet.
    """

    success = Boolean(description="Verifica se ocorreu tudo ok.")

    class Arguments:
        """
        Define os dados que você pode enviar para o servidor.
        """

        identify = Int(
            description="Identificador do pet.",
            required=True
        )

    def mutate(self, info, identify):
        """
        Mutações
        """

        logged_user = GenericUtils.get_logged_user(info)

        GenericPermissions.auth_validation(logged_user)

        DeletePetsResolver(logged_user, identify).get_result()

        return DeletePetMutation(success=True)
