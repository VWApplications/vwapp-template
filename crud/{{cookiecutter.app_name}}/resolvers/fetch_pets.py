from petguard.pets.models import Pet
from django.contrib.auth import get_user_model

User = get_user_model()


class FetchPetResolver:
    """
    Classe responsável pela lógica de pegar um pet de um usuário.
    """

    def __init__(self, identify, pet_id):
        """
        Construtor
        """

        self.identify = identify
        self.pet_id = pet_id

    def get_result(self):
        """
        Resultado do resolver.
        """

        account = User.objects.get_user(self.identify)

        user, ong = Pet.objects.get_user_type(account)

        if ong:
            pet = Pet.objects.get_pet_ong(self.pet_id, user)
        else:
            pet = Pet.objects.get_pet(self.pet_id, user)

        return pet
