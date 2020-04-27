from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from common.test_utils import GenericTestUtils
from petguard.users.models import PetGuardUser, PetGuardPartner
from petguard.users.models.petguard_user import insert_qrcode_to_account
from petguard.pets.models import Pet, Alimentation, SpecialCares

User = get_user_model()


class DeletePetsTestCase(TestCase):
    """
    Teste para deletar um pet no sistema
    """

    def setUp(self):
        """
        Método que roda a cada teste
        """

        post_save.disconnect(insert_qrcode_to_account, sender=PetGuardUser, dispatch_uid='insert_qrcode_to_account')

        user1 = User.objects.create_user(
            username='fulano1',
            name='Fulano1',
            email='fulano1@gmail.com',
            password='django1234'
        )
        self.petguard_user1 = PetGuardUser.objects.create(account=user1)

        user2 = User.objects.create_user(
            username='fulano2',
            name='Fulano2',
            email='fulano2@gmail.com',
            password='django1234'
        )
        self.petguard_user2 = PetGuardUser.objects.create(account=user2)

        partner1 = User.objects.create_user(
            username='ong1',
            name='Ong1',
            email='ong1@gmail.com',
            password='django1234'
        )
        self.petguard_partner1 = PetGuardPartner.objects.create(account=partner1)

        partner2 = User.objects.create_user(
            username='ong2',
            name='Ong2',
            email='ong2@gmail.com',
            password='django1234'
        )
        self.petguard_partner2 = PetGuardPartner.objects.create(account=partner2)

        alimentation1 = Alimentation.objects.create(
            qtd="SMALL",
            food="pedigree",
            frequency=2
        )

        special_cares1 = SpecialCares.objects.create(
            veterinary_frequency=2,
            bathing_frequency=1
        )

        self.pet1 = Pet.objects.create(
            owner=self.petguard_user1,
            name="XU",
            kind="DOG",
            sex="FEMALE",
            height="SMALL",
            temperament="FRIENDLY",
            alimentation=alimentation1,
            special_cares=special_cares1
        )

        alimentation2 = Alimentation.objects.create(
            qtd="SMALL",
            food="pedigree",
            frequency=2
        )

        special_cares2 = SpecialCares.objects.create(
            veterinary_frequency=2,
            bathing_frequency=1
        )

        self.pet2 = Pet.objects.create(
            owner=self.petguard_user2,
            name="XU",
            kind="DOG",
            sex="FEMALE",
            height="SMALL",
            temperament="FRIENDLY",
            alimentation=alimentation2,
            special_cares=special_cares2
        )

        alimentation3 = Alimentation.objects.create(
            qtd="SMALL",
            food="pedigree",
            frequency=2
        )

        special_cares3 = SpecialCares.objects.create(
            veterinary_frequency=2,
            bathing_frequency=1
        )

        self.pet3 = Pet.objects.create(
            ong=self.petguard_partner1,
            name="XU",
            kind="DOG",
            sex="FEMALE",
            height="SMALL",
            temperament="FRIENDLY",
            alimentation=alimentation3,
            special_cares=special_cares3
        )

        alimentation4 = Alimentation.objects.create(
            qtd="SMALL",
            food="pedigree",
            frequency=2
        )

        special_cares4 = SpecialCares.objects.create(
            veterinary_frequency=2,
            bathing_frequency=1
        )

        self.pet4 = Pet.objects.create(
            ong=self.petguard_partner2,
            name="XU",
            kind="DOG",
            sex="FEMALE",
            height="SMALL",
            temperament="FRIENDLY",
            alimentation=alimentation4,
            special_cares=special_cares4
        )

        self.query = """
            mutation DeletePets($identify: Int!) {
                petguard {
                    pets {
                        delete_pet(identify: $identify) {
                            success
                        }
                    }
                }
            }
        """

        self.variables = {'identify': self.pet1.id}

        self.request = GenericTestUtils.authenticate(self.petguard_user1.account)

        self.maxDiff = None

    def tearDown(self):
        """
        This method will run after any test.
        """

        SpecialCares.objects.all().delete()
        Alimentation.objects.all().delete()
        Pet.objects.all().delete()
        PetGuardPartner.objects.all().delete()
        PetGuardUser.objects.all().delete()
        User.objects.all().delete()

    def test_delete_pet(self):
        """
        Deleta um pet normalmente.
        """

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "delete_pet": {
                            "success": True
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 3)
        self.assertEqual(SpecialCares.objects.count(), 3)
        self.assertEqual(Alimentation.objects.count(), 3)

    def test_delete_pet_ong(self):
        """
        Ong deleta um pet normalmente.
        """

        variables = {'identify': self.pet3.id}

        request = GenericTestUtils.authenticate(self.petguard_partner1.account)

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "delete_pet": {
                            "success": True
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=request
        )

        self.assertEqual(Pet.objects.count(), 3)
        self.assertEqual(SpecialCares.objects.count(), 3)
        self.assertEqual(Alimentation.objects.count(), 3)

    def test_delete_another_user_pet(self):
        """
        Usuário não pode deletar o pet de outras usuários.
        """

        self.variables['identify'] = self.pet2.id

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet2.id}"
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

    def test_delete_another_ong_pet(self):
        """
        Usuário não pode deletar o pet de parceiros.
        """

        self.variables['identify'] = self.pet3.id

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet3.id}"
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

    def test_ong_delete_another_user_pet(self):
        """
        Ong não pode deletar o pet de outras usuários.
        """

        request = GenericTestUtils.authenticate(self.petguard_partner1.account)

        self.variables['identify'] = self.pet1.id

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet1.id}"
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=request
        )

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

    def test_ong_delete_another_ong_pet(self):
        """
        Ong não pode deletar o pet de parceiros.
        """

        request = GenericTestUtils.authenticate(self.petguard_partner1.account)

        self.variables['identify'] = self.pet4.id

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet4.id}"
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=request
        )

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

    def test_delete_invalid_pet(self):
        """
        Não pode deletar o pet de outras pessoas.
        """

        self.variables['identify'] = 20

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: 20"
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

    def test_not_logged_user(self):
        """
        Usuário não logado não pode deletar pet.
        """

        result = {
            "status": 400,
            "error": {
                "message": "Usuário precisa está autenticado para realizar essa ação.",
                "cause": "Usuário não está autenticado no sistema."
            }
        }

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables
        )

        self.assertEqual(Pet.objects.count(), 4)
        self.assertEqual(Alimentation.objects.count(), 4)
        self.assertEqual(SpecialCares.objects.count(), 4)
