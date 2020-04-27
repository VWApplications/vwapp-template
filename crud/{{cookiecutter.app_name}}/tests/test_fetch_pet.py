from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from common.test_utils import GenericTestUtils
from petguard.users.models import PetGuardUser, PetGuardPartner
from petguard.users.models.petguard_user import insert_qrcode_to_account
from petguard.pets.models import Pet, Alimentation, SpecialCares

User = get_user_model()


class FetchPetTestCase(TestCase):
    """
    Teste para pegar um pet de um usuário no sistema.
    """

    def setUp(self):
        """
        Método que roda a cada teste
        """

        post_save.disconnect(insert_qrcode_to_account, sender=PetGuardUser, dispatch_uid='insert_qrcode_to_account')

        user1 = User.objects.create_user(
            email='fulano01@gmail.com',
            username='fulano01',
            name='Fulano 01',
            password='django1234'
        )
        self.user1 = PetGuardUser.objects.create(account=user1)

        user2 = User.objects.create(
            email='fulano02@gmail.com',
            username='fulano02',
            name='Fulano 02',
            password='django1234',
            is_active=False
        )
        self.user2 = PetGuardUser.objects.create(account=user2)

        self.user3 = User.objects.create_user(
            email='fulano03@gmail.com',
            username='fulano03',
            name='Fulano 03',
            password='django1234'
        )

        partner1 = User.objects.create_user(
            email='ong01@gmail.com',
            username='ong01',
            name='Ong 01',
            password='django1234'
        )
        self.partner1 = PetGuardPartner.objects.create(account=partner1)

        partner2 = User.objects.create_user(
            email='ong02@gmail.com',
            username='ong02',
            name='Ong 02',
            password='django1234'
        )
        self.partner2 = PetGuardPartner.objects.create(account=partner2)

        self.partner3 = User.objects.create_user(
            email='ong03@gmail.com',
            username='ong03',
            name='Ong 03',
            password='django1234'
        )

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
            owner=self.user1,
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
            owner=self.user2,
            name="PUFF",
            kind="DOG",
            sex="MALE",
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
            ong=self.partner1,
            name="PUFF",
            kind="DOG",
            sex="MALE",
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
            ong=self.partner2,
            name="PUFF",
            kind="DOG",
            sex="MALE",
            height="SMALL",
            temperament="FRIENDLY",
            alimentation=alimentation4,
            special_cares=special_cares4
        )

        self.query = """
            query FetchPet($identify: String!, $pet_id: String!) {
                petguard {
                    pets {
                        instance(identify: $identify, pet_id: $pet_id) {
                            name
                        }
                    }
                }
            }
        """

        self.variables = {
            "identify": self.user1.account.email,
            "pet_id": self.pet1.id
        }

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

    def test_fetch_pet(self):
        """
        Pegar informações de um pet pelo seu id
        """

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "instance": {
                            "name": "XU",
                        }
                    }
                }
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables
        )

    def test_fetch_ong_pet(self):
        """
        Pegar informações de um pet para adoção pelo seu id.
        """

        variables = {
            "identify": self.pet3.ong.account.email,
            "pet_id": self.pet3.id
        }

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "instance": {
                            "name": "PUFF",
                        }
                    }
                }
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables
        )

    def test_fetch_pet_another_user(self):
        """
        Tentando encontrar um pet que não existe para um usuário
        """

        self.variables['pet_id'] = self.pet2.id

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet2.id}"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables
        )

    def test_fetch_pet_another_ong(self):
        """
        Tentando encontrar um pet que não existe para uma ong.
        """

        variables = {
            "identify": self.pet3.ong.account.email,
            "pet_id": self.pet4.id
        }

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet4.id}"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables
        )

    def test_fetch_not_exist_petguard_user(self):
        """
        Usuário que não tem conta na pet guard não pode pesquisar seus dados.
        """

        self.variables['identify'] = self.user3.email

        result = {
            "status": 400,
            "error": {
                "message": "Usuário não tem conta no petguard.",
                "cause": f"Usuário {self.user3.email} não tem contan no petguard."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables
        )

    def test_fetch_not_exist_petguard_partner(self):
        """
        Ong que não tem conta na pet guard não pode pesquisar seus dados.
        """

        variables = {
            "identify": self.partner3.email,
            "pet_id": self.pet3.id
        }

        result = {
            "status": 400,
            "error": {
                "message": "Usuário não tem conta no petguard.",
                "cause": f"Usuário {self.partner3.email} não tem contan no petguard."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables
        )

    def test_logged_user_can_see_pet_details(self):
        """
        Usuário logado por ver detalhes de seu pet.
        """

        request = GenericTestUtils.authenticate(self.user1.account)

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "instance": {
                            "name": "XU",
                        }
                    }
                }
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=request
        )

    def test_logged_user_can_see_ong_pet_details(self):
        """
        Usuário logado por ver detalhes do pet de uma ong.
        """

        request = GenericTestUtils.authenticate(self.user1.account)

        variables = {
            "identify": self.partner1.account.email,
            "pet_id": self.pet3.id
        }

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "instance": {
                            "name": "PUFF",
                        }
                    }
                }
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=request
        )

    def test_logged_ong_can_see_ong_pet_details(self):
        """
        Ong logado por ver detalhes do seu pet.
        """

        request = GenericTestUtils.authenticate(self.partner1.account)

        variables = {
            "identify": self.partner1.account.email,
            "pet_id": self.pet3.id
        }

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "instance": {
                            "name": "PUFF",
                        }
                    }
                }
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=request
        )
