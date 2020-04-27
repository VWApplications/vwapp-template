from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from common.test_utils import GenericTestUtils
from petguard.users.models import PetGuardUser, PetGuardPartner
from petguard.users.models.petguard_user import insert_qrcode_to_account
from petguard.pets.models import Pet, Alimentation, SpecialCares
from vwapp.settings import BASE_DIR
from datetime import datetime, timedelta
import shutil

User = get_user_model()


class CreatePetsTestCase(TestCase):
    """
    Teste para cadastrar um pet no sistema
    """

    def setUp(self):
        """
        Método que roda a cada teste
        """

        post_save.disconnect(insert_qrcode_to_account, sender=PetGuardUser, dispatch_uid='insert_qrcode_to_account')

        user1 = User.objects.create_user(
            username='fulano',
            name='Fulano',
            email='fulano@gmail.com',
            password='django1234'
        )

        self.petguard_user = PetGuardUser.objects.create(account=user1)

        user2 = User.objects.create_user(
            username='ong',
            name='Ong',
            email='ong@gmail.com',
            password='django1234'
        )

        self.petguard_partner = PetGuardPartner.objects.create(account=user2)

        self.query = """
            mutation CreatePets($data: CreatePetInput!) {
                petguard {
                    pets {
                        create_pet(data: $data) {
                            pet {
                                name
                                kind
                                sex
                                height
                                temperament
                                alimentation {
                                    qtd
                                    food
                                    frequency
                                }
                                special_cares {
                                    veterinary_frequency
                                    bathing_frequency
                                }
                            }
                        }
                    }
                }
            }
        """

        self.variables = {
            'data': {
                'name': "XU",
                'kind': "DOG",
                'sex': "FEMALE",
                'height': "SMALL",
                'temperament': "FRIENDLY",
                'alimentation': {
                    'qtd': "SMALL",
                    'food': "pedigree",
                    'frequency': 2
                },
                'special_cares': {
                    'veterinary_frequency': 2,
                    'bathing_frequency': 1
                }
            }
        }

        self.request = GenericTestUtils.authenticate(self.petguard_user.account)

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

    def test_create_pet_user(self):
        """
        Criando um pet para usuários.
        """

        query = """
            mutation CreatePets($data: CreatePetInput!) {
                petguard {
                    pets {
                        create_pet(data: $data) {
                            pet {
                                name
                                kind
                                sex
                                height
                                temperament
                                photo {
                                    name
                                }
                                alimentation {
                                    qtd
                                    food
                                    frequency
                                }
                                special_cares {
                                    veterinary_frequency
                                    bathing_frequency
                                }
                            }
                        }
                    }
                }
            }
        """

        avatar = GenericTestUtils.create_image(None, 'pet.png')
        avatar_file = SimpleUploadedFile("pet.png", avatar.getvalue())

        self.variables['data']['photo'] = avatar_file

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "create_pet": {
                            "pet": {
                                'name': "XU",
                                'kind': "DOG",
                                'sex': "FEMALE",
                                'height': "SMALL",
                                'temperament': "FRIENDLY",
                                'photo': {'name': 'petguard_pets/pet.png'},
                                'alimentation': {
                                    'qtd': "SMALL",
                                    'food': "pedigree",
                                    'frequency': 2
                                },
                                'special_cares': {
                                    'veterinary_frequency': 2,
                                    'bathing_frequency': 1
                                }
                            }
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertTrue(Pet.objects.last().photo)
        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(Alimentation.objects.count(), 1)
        self.assertEqual(SpecialCares.objects.count(), 1)
        self.assertEqual(Pet.objects.last().owner, self.petguard_user)
        self.assertEqual(Pet.objects.last().ong, None)

        # Remove all image files created
        shutil.rmtree(f"{BASE_DIR}/mediafiles/petguard_pets")

    def test_create_pet_partner(self):
        """
        Criando um pet para ongs.
        """

        request = GenericTestUtils.authenticate(self.petguard_partner.account)

        query = """
            mutation CreatePets($data: CreatePetInput!) {
                petguard {
                    pets {
                        create_pet(data: $data) {
                            pet {
                                name
                                kind
                                sex
                                height
                                temperament
                                photo {
                                    name
                                }
                                alimentation {
                                    qtd
                                    food
                                    frequency
                                }
                                special_cares {
                                    veterinary_frequency
                                    bathing_frequency
                                }
                            }
                        }
                    }
                }
            }
        """

        avatar = GenericTestUtils.create_image(None, 'pet.png')
        avatar_file = SimpleUploadedFile("pet.png", avatar.getvalue())

        self.variables['data']['photo'] = avatar_file

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "create_pet": {
                            "pet": {
                                'name': "XU",
                                'kind': "DOG",
                                'sex': "FEMALE",
                                'height': "SMALL",
                                'temperament': "FRIENDLY",
                                'photo': {'name': 'petguard_pets/pet.png'},
                                'alimentation': {
                                    'qtd': "SMALL",
                                    'food': "pedigree",
                                    'frequency': 2
                                },
                                'special_cares': {
                                    'veterinary_frequency': 2,
                                    'bathing_frequency': 1
                                }
                            }
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=query,
            data=result,
            variables=self.variables,
            context=request
        )

        self.assertTrue(Pet.objects.last().photo)
        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(Alimentation.objects.count(), 1)
        self.assertEqual(SpecialCares.objects.count(), 1)
        self.assertEqual(Pet.objects.last().owner, None)
        self.assertEqual(Pet.objects.last().ong, self.petguard_partner)

        # Remove all image files created
        shutil.rmtree(f"{BASE_DIR}/mediafiles/petguard_pets")

    def test_required_name(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['name'] = ''

        result = {
            "status": 400,
            "error": {
                "message": "Campo name não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_age(self):
        """
        Idade não pode ter valores negativos.
        """

        self.variables['data']['age'] = -1

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_kind(self):
        """
        Só pode alguns tipo de animais como CAT e DOG.
        """

        self.variables['data']['kind'] = 'FISH'

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: FISH"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_required_kind(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['kind'] = ''

        result = {
            "status": 400,
            "error": {
                "message": "Campo kind não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_sex(self):
        """
        Só pode 2 tipos de sexo como FEMALE e MALE.
        """

        self.variables['data']['sex'] = 'OGRO'

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: OGRO"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_required_sex(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['sex'] = ''

        result = {
            "status": 400,
            "error": {
                "message": "Campo sex não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_height(self):
        """
        Só pode alguns tipos de porte como SMALL e MEDIUM, BIG.
        """

        self.variables['data']['height'] = 'GORDO'

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: GORDO"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_required_height(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['height'] = ''

        result = {
            "status": 400,
            "error": {
                "message": "Campo height não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_temperament(self):
        """
        Só pode alguns tipos de temperamento como DOCILE, FRIENDLY e BRAVE.
        """

        self.variables['data']['temperament'] = 'SEILA'

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: SEILA"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_required_temperament(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['temperament'] = ''

        result = {
            "status": 400,
            "error": {
                "message": "Campo temperament não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_weight(self):
        """
        Peso não pode ter valores negativos.
        """

        self.variables['data']['weight'] = -1

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1.0"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_alimentation_qtd(self):
        """
        Só pode alguns tipos de quantidade de alimentos como SMALL, MEDIUM e BIG.
        """

        self.variables['data']['alimentation']['qtd'] = 'OLOKO'

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: OLOKO"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_required_alimentation_qtd(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['alimentation']['qtd'] = ''

        result = {
            "status": 400,
            "error": {
                "message": "Campo qtd não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_required_alimentation_food(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['alimentation']['food'] = ''

        result = {
            "status": 400,
            "error": {
                "message": "Campo food não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_required_alimentation_frequency(self):
        """
        Atributo é obrigatório
        """

        self.variables['data']['alimentation']['frequency'] = 0

        result = {
            "status": 400,
            "error": {
                "message": "Campo frequency não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_alimentation_frequency(self):
        """
        A frequência de alimentação não pode ter valores negativos.
        """

        self.variables['data']['alimentation']['frequency'] = -1

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_create_pet_without_alimentation(self):
        """
        Criando um pet normalmente sem a alimentação.
        """

        self.variables['data']['alimentation'] = None

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "create_pet": {
                            "pet": {
                                'name': "XU",
                                'kind': "DOG",
                                'sex': "FEMALE",
                                'height': "SMALL",
                                'temperament': "FRIENDLY",
                                'alimentation': None,
                                'special_cares': {
                                    'veterinary_frequency': 2,
                                    'bathing_frequency': 1
                                }
                            }
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 1)

    def test_create_pet_without_special_cares(self):
        """
        Criando um pet normalmente sem a cuidados especiais.
        """

        self.variables['data']['special_cares'] = None

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "create_pet": {
                            "pet": {
                                'name': "XU",
                                'kind': "DOG",
                                'sex': "FEMALE",
                                'height': "SMALL",
                                'temperament': "FRIENDLY",
                                'alimentation': {
                                    'qtd': "SMALL",
                                    'food': "pedigree",
                                    'frequency': 2
                                },
                                'special_cares': None
                            }
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(Alimentation.objects.count(), 1)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_create_pet_without_alimentation_and_special_cares(self):
        """
        Criando um pet normalmente sem a alimentação e cuidados especiais.
        """

        self.variables['data']['alimentation'] = None
        self.variables['data']['special_cares'] = None

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "create_pet": {
                            "pet": {
                                'name': "XU",
                                'kind': "DOG",
                                'sex': "FEMALE",
                                'height': "SMALL",
                                'temperament': "FRIENDLY",
                                'alimentation': None,
                                'special_cares': None,
                            }
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_special_cares_veterinary_frequency(self):
        """
        A frequência de ida ao veterinário não pode ter valores negativos.
        """

        self.variables['data']['special_cares']['veterinary_frequency'] = -1

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_special_cares_bathing_frequency(self):
        """
        A frequência de banho não pode ter valores negativos.
        """

        self.variables['data']['special_cares']['bathing_frequency'] = -1

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_special_cares_shear_frequency(self):
        """
        A frequência de tosa não pode ter valores negativos.
        """

        self.variables['data']['special_cares']['shear_frequency'] = -1

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_create_pet_with_date(self):
        """
        Criando um pet com valores de data.
        """

        query = """
            mutation CreatePets($data: CreatePetInput!) {
                petguard {
                    pets {
                        create_pet(data: $data) {
                            pet {
                                name
                                special_cares {
                                    deworming_date
                                    vaccination_date
                                    last_estro
                                }
                            }
                        }
                    }
                }
            }
        """

        self.variables['data']['special_cares']['deworming_date'] = "2020-02-21"
        self.variables['data']['special_cares']['vaccination_date'] = "2020-02-22"
        self.variables['data']['special_cares']['last_estro'] = "2020-02-23"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "create_pet": {
                            "pet": {
                                'name': "XU",
                                'special_cares': {
                                    'deworming_date': "2020-02-21",
                                    'vaccination_date': "2020-02-22",
                                    'last_estro': "2020-02-23"
                                }
                            }
                        }
                    }
                }
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(Alimentation.objects.count(), 1)
        self.assertEqual(SpecialCares.objects.count(), 1)

    def test_invalid_special_cares_deworming_date(self):
        """
        A data passada está inválida.
        """

        self.variables['data']['special_cares']['deworming_date'] = "2020-02-31"

        result = {
            "status": 400,
            "error": {
                "message": "O dia passado está incorreto. Tem que está entre 1 e 29",
                "cause": "Valor passado: 31"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_special_cares_vaccination_date(self):
        """
        A data passada está inválida.
        """

        self.variables['data']['special_cares']['vaccination_date'] = "2020-13-02"

        result = {
            "status": 400,
            "error": {
                "message": "O mês passado está incorreto. Tem que está entre 1 e 12",
                "cause": "Valor passado: 13"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_special_cares_last_estro(self):
        """
        A data passada está inválida.
        """

        self.variables['data']['special_cares']['last_estro'] = "2020-13-022"

        result = {
            "status": 400,
            "error": {
                "message": "A data passada está no formato errado. Formato correto: YYYY-MM-DD",
                "cause": "Valor passado: 2020-13-022"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_invalid_before_date_special_cares_last_estro(self):
        """
        A data passada está após a data atual.
        """

        future = datetime.now() + timedelta(days=365)

        self.variables['data']['special_cares']['last_estro'] = f"{future.year}-03-03"

        result = {
            "status": 400,
            "error": {
                "message": "A data passada tem que ser antes da data atual.",
                "cause": f"Valor passado: {future.year}-03-03"
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables,
            context=self.request
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

    def test_not_logged_user(self):
        """
        Usuário não logado não pode criar pet.
        """

        result = {
            "status": 400,
            "error": {
                "message": "Usuário precisa está autenticado para realizar essa ação.",
                "cause": "Usuário não está autenticado no sistema."
            }
        }

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=self.variables
        )

        self.assertEqual(Pet.objects.count(), 0)
        self.assertEqual(Alimentation.objects.count(), 0)
        self.assertEqual(SpecialCares.objects.count(), 0)
