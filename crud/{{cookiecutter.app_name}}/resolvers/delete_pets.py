from petguard.pets.models import Pet


class DeletePetsResolver:
    """
    Classe responsável pela lógica de deleção de pets
    """

    def __init__(self, user, identify):
        """
        Construtor
        """

        self.user, self.ong = Pet.objects.get_user_type(user)
        self.identify = identify

    def get_result(self):
        """
        Resultado do resolver.
        """

        if self.ong:
            pet = Pet.objects.get_pet_ong(self.identify, self.user)
        else:
            pet = Pet.objects.get_pet(self.identify, self.user)

        if pet.alimentation:
            pet.alimentation.delete()

        if pet.special_cares:
            pet.special_cares.delete()

        pet.delete()
