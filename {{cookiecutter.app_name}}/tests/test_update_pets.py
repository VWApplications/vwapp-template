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


class UpdatePetsTestCase(TestCase):
    """
    Teste para atualizar um pet no sistema
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
            name='Ong 1',
            email='ong1@gmail.com',
            password='django1234'
        )
        self.petguard_partner1 = PetGuardPartner.objects.create(account=partner1)

        partner2 = User.objects.create_user(
            username='ong2',
            name='Ong 2',
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
            mutation UpdatePets($data: UpdatePetInput!, $identify: Int!) {
                petguard {
                    pets {
                        update_pet(identify: $identify, data: $data) {
                            pet {
                                name
                            }
                        }
                    }
                }
            }
        """

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

    def test_update_pet(self):
        """
        Atualiza um pet normalmente.
        """

        query = """
            mutation UpdatePets($data: UpdatePetInput!, $identify: Int!) {
                petguard {
                    pets {
                        update_pet(identify: $identify, data: $data) {
                            pet {
                                name
                                kind
                                sex
                                height
                                temperament
                                age
                                breed
                                photo {
                                    name
                                }
                                phone
                                weight
                                description
                                alimentation {
                                    qtd
                                    food
                                    frequency
                                    observations
                                }
                                special_cares {
                                    veterinary_frequency
                                    bathing_frequency
                                    diseases
                                    shear_type
                                    shear_frequency
                                    deworming
                                    deworming_date
                                    vaccination
                                    vaccination_date
                                    is_castrated
                                    last_estro
                                    observations
                                    veterinary_feedback
                                }
                            }
                        }
                    }
                }
            }
        """

        avatar = GenericTestUtils.create_image(None, 'updated_pet.png')
        avatar_file = SimpleUploadedFile("updated_pet.png", avatar.getvalue())

        variables = {
            'identify': self.pet1.id,
            'data': {
                'name': "XU",
                'kind': "DOG",
                'sex': "FEMALE",
                'height': "SMALL",
                'temperament': "FRIENDLY",
                'age': 7,
                'breed': "Poodle",
                'photo': avatar_file,
                'phone': "61999824945",
                'weight': 15.4,
                'description': "Baixinha arretada.",
                'alimentation': {
                    'qtd': "SMALL",
                    'food': "pedigree",
                    'frequency': 2,
                    'observations': "Ela come sozinha. Só deixar a ração aberta e acessível."
                },
                'special_cares': {
                    'veterinary_frequency': 2,
                    'bathing_frequency': 1,
                    'diseases': "Ela se engasga as vezes.",
                    'shear_type': "Raspa tudo.",
                    'shear_frequency': 60,
                    'deworming': "Vermifugação muito doida.",
                    'deworming_date': "2020-02-23",
                    'vaccination': "Vacina muito doida.",
                    'vaccination_date': "2020-02-24",
                    'is_castrated': True,
                    'last_estro': "2020-01-12",
                    'observations': "Ela se acostuma muito rápido com as pessoas.",
                    'veterinary_feedback': "Ela morde se ela se sentir ameaçada."
                }
            }
        }

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "update_pet": {
                            "pet": {
                                'name': "XU",
                                'kind': "DOG",
                                'sex': "FEMALE",
                                'height': "SMALL",
                                'temperament': "FRIENDLY",
                                'age': 7,
                                'breed': "Poodle",
                                'photo': {'name': 'petguard_pets/updated_pet.png'},
                                'phone': "61999824945",
                                'weight': 15.4,
                                'description': "Baixinha arretada.",
                                'alimentation': {
                                    'qtd': "SMALL",
                                    'food': "pedigree",
                                    'frequency': 2,
                                    'observations': "Ela come sozinha. Só deixar a ração aberta e acessível."
                                },
                                'special_cares': {
                                    'veterinary_frequency': 2,
                                    'bathing_frequency': 1,
                                    'diseases': "Ela se engasga as vezes.",
                                    'shear_type': "Raspa tudo.",
                                    'shear_frequency': 60,
                                    'deworming': "Vermifugação muito doida.",
                                    'deworming_date': "2020-02-23",
                                    'vaccination': "Vacina muito doida.",
                                    'vaccination_date': "2020-02-24",
                                    'is_castrated': True,
                                    'last_estro': "2020-01-12",
                                    'observations': "Ela se acostuma muito rápido com as pessoas.",
                                    'veterinary_feedback': "Ela morde se ela se sentir ameaçada."
                                }
                            }
                        }
                    }
                }
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=query,
            data=result,
            variables=variables,
            context=self.request
        )

        # Remove all image files created
        shutil.rmtree(f"{BASE_DIR}/mediafiles/petguard_pets")

    def test_update_ong_pet(self):
        """
        Atualiza um pet de uma ong normalmente.
        """

        request = GenericTestUtils.authenticate(self.petguard_partner1.account)

        query = """
            mutation UpdatePets($data: UpdatePetInput!, $identify: Int!) {
                petguard {
                    pets {
                        update_pet(identify: $identify, data: $data) {
                            pet {
                                name
                                kind
                                sex
                                height
                                temperament
                                age
                                breed
                                photo {
                                    name
                                }
                                phone
                                weight
                                description
                                alimentation {
                                    qtd
                                    food
                                    frequency
                                    observations
                                }
                                special_cares {
                                    veterinary_frequency
                                    bathing_frequency
                                    diseases
                                    shear_type
                                    shear_frequency
                                    deworming
                                    deworming_date
                                    vaccination
                                    vaccination_date
                                    is_castrated
                                    last_estro
                                    observations
                                    veterinary_feedback
                                }
                            }
                        }
                    }
                }
            }
        """

        avatar = GenericTestUtils.create_image(None, 'updated_pet.png')
        avatar_file = SimpleUploadedFile("updated_pet.png", avatar.getvalue())

        variables = {
            'identify': self.pet3.id,
            'data': {
                'name': "XU",
                'kind': "DOG",
                'sex': "FEMALE",
                'height': "SMALL",
                'temperament': "FRIENDLY",
                'age': 7,
                'breed': "Poodle",
                'photo': avatar_file,
                'phone': "61999824945",
                'weight': 15.4,
                'description': "Baixinha arretada.",
                'alimentation': {
                    'qtd': "SMALL",
                    'food': "pedigree",
                    'frequency': 2,
                    'observations': "Ela come sozinha. Só deixar a ração aberta e acessível."
                },
                'special_cares': {
                    'veterinary_frequency': 2,
                    'bathing_frequency': 1,
                    'diseases': "Ela se engasga as vezes.",
                    'shear_type': "Raspa tudo.",
                    'shear_frequency': 60,
                    'deworming': "Vermifugação muito doida.",
                    'deworming_date': "2020-02-23",
                    'vaccination': "Vacina muito doida.",
                    'vaccination_date': "2020-02-24",
                    'is_castrated': True,
                    'last_estro': "2020-01-12",
                    'observations': "Ela se acostuma muito rápido com as pessoas.",
                    'veterinary_feedback': "Ela morde se ela se sentir ameaçada."
                }
            }
        }

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "update_pet": {
                            "pet": {
                                'name': "XU",
                                'kind': "DOG",
                                'sex': "FEMALE",
                                'height': "SMALL",
                                'temperament': "FRIENDLY",
                                'age': 7,
                                'breed': "Poodle",
                                'photo': {'name': 'petguard_pets/updated_pet.png'},
                                'phone': "61999824945",
                                'weight': 15.4,
                                'description': "Baixinha arretada.",
                                'alimentation': {
                                    'qtd': "SMALL",
                                    'food': "pedigree",
                                    'frequency': 2,
                                    'observations': "Ela come sozinha. Só deixar a ração aberta e acessível."
                                },
                                'special_cares': {
                                    'veterinary_frequency': 2,
                                    'bathing_frequency': 1,
                                    'diseases': "Ela se engasga as vezes.",
                                    'shear_type': "Raspa tudo.",
                                    'shear_frequency': 60,
                                    'deworming': "Vermifugação muito doida.",
                                    'deworming_date': "2020-02-23",
                                    'vaccination': "Vacina muito doida.",
                                    'vaccination_date': "2020-02-24",
                                    'is_castrated': True,
                                    'last_estro': "2020-01-12",
                                    'observations': "Ela se acostuma muito rápido com as pessoas.",
                                    'veterinary_feedback': "Ela morde se ela se sentir ameaçada."
                                }
                            }
                        }
                    }
                }
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=query,
            data=result,
            variables=variables,
            context=request
        )

        # Remove all image files created
        shutil.rmtree(f"{BASE_DIR}/mediafiles/petguard_pets")

    def test_required_name(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'name': ""}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo name não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("XU", self.pet1.name)

    def test_invalid_age(self):
        """
        Idade não pode ter valores negativos.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'age': -1}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(None, self.pet1.age)

    def test_invalid_kind(self):
        """
        Só pode alguns tipo de animais como CAT e DOG.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'kind': 'FISH'}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: FISH"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("DOG", self.pet1.kind)

    def test_required_kind(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'kind': ''}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo kind não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("DOG", self.pet1.kind)

    def test_invalid_sex(self):
        """
        Só pode 2 tipos de sexo como FEMALE e MALE.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'sex': 'OGRO'}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: OGRO"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("FEMALE", self.pet1.sex)

    def test_required_sex(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'sex': ''}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo sex não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("FEMALE", self.pet1.sex)

    def test_invalid_height(self):
        """
        Só pode alguns tipos de porte como SMALL e MEDIUM, BIG.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'height': 'GORDO'}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: GORDO"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("SMALL", self.pet1.height)

    def test_required_height(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'height': ''}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo height não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("SMALL", self.pet1.height)

    def test_invalid_temperament(self):
        """
        Só pode alguns tipos de temperamento como DOCILE, FRIENDLY e BRAVE.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'temperament': 'SEILA'}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: SEILA"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("FRIENDLY", self.pet1.temperament)

    def test_required_temperament(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'temperament': ''}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo temperament não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("FRIENDLY", self.pet1.temperament)

    def test_invalid_weight(self):
        """
        Peso não pode ter valores negativos.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'weight': -1}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1.0"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(None, self.pet1.weight)

    def test_invalid_alimentation_qtd(self):
        """
        Só pode alguns tipos de quantidade de alimentos como SMALL, MEDIUM e BIG.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'alimentation': {'qtd': 'OLOKO'}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não consta nos valores definidos no sistema.",
                "cause": "Valor passado: OLOKO"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("SMALL", self.pet1.alimentation.qtd)

    def test_required_alimentation_qtd(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'alimentation': {'qtd': ''}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo qtd não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("SMALL", self.pet1.alimentation.qtd)

    def test_required_alimentation_food(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'alimentation': {'food': ''}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo food não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual("pedigree", self.pet1.alimentation.food)

    def test_required_alimentation_frequency(self):
        """
        Atributo é obrigatório
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'alimentation': {'frequency': 0}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Campo frequency não pode ser vazio.",
                "cause": "Valor passado está vazio."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(2, self.pet1.alimentation.frequency)

    def test_invalid_alimentation_frequency(self):
        """
        A frequência de alimentação não pode ter valores negativos.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'alimentation': {'frequency': -1}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(2, self.pet1.alimentation.frequency)

    def test_invalid_special_cares_veterinary_frequency(self):
        """
        A frequência de ida ao veterinário não pode ter valores negativos.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'special_cares': {'veterinary_frequency': -1}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(2, self.pet1.special_cares.veterinary_frequency)

    def test_invalid_special_cares_bathing_frequency(self):
        """
        A frequência de banho não pode ter valores negativos.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'special_cares': {'bathing_frequency': -1}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(1, self.pet1.special_cares.bathing_frequency)

    def test_invalid_special_cares_shear_frequency(self):
        """
        A frequência de tosa não pode ter valores negativos.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'special_cares': {'shear_frequency': -1}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O valor passado não pode ser negativo.",
                "cause": "Valor passado: -1"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(0, self.pet1.special_cares.shear_frequency)

    def test_invalid_special_cares_deworming_date(self):
        """
        A data passada está inválida.
        """

        variables = {
            'identify': self.pet2.id,
            'data': {'special_cares': {'deworming_date': "2020-02-31"}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O dia passado está incorreto. Tem que está entre 1 e 29",
                "cause": "Valor passado: 31"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(None, self.pet1.special_cares.deworming_date)

    def test_invalid_special_cares_vaccination_date(self):
        """
        A data passada está inválida.
        """

        variables = {
            'identify': self.pet2.id,
            'data': {'special_cares': {'vaccination_date': "2020-13-02"}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "O mês passado está incorreto. Tem que está entre 1 e 12",
                "cause": "Valor passado: 13"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(None, self.pet1.special_cares.vaccination_date)

    def test_invalid_special_cares_last_estro(self):
        """
        A data passada está inválida.
        """

        variables = {
            'identify': self.pet2.id,
            'data': {'special_cares': {'last_estro': "2020-13-022"}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "A data passada está no formato errado. Formato correto: YYYY-MM-DD",
                "cause": "Valor passado: 2020-13-022"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(None, self.pet1.special_cares.last_estro)

    def test_invalid_before_date_special_cares_last_estro(self):
        """
        A data passada está após a data atual.
        """

        future = datetime.now() + timedelta(days=365)

        variables = {
            'identify': self.pet2.id,
            'data': {'special_cares': {'last_estro': f"{future.year}-03-03"}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "A data passada tem que ser antes da data atual.",
                "cause": f"Valor passado: {future.year}-03-03"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(None, self.pet1.special_cares.last_estro)

    def test_invalid_pet_identify(self):
        """
        O pet tem que ser do usuário que irá edita-lo.
        """

        variables = {
            'identify': self.pet3.id,
            'data': {'special_cares': {'shear_frequency': 2}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet3.id}"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=self.request
        )

        self.pet3.refresh_from_db()
        self.assertEqual(0, self.pet3.special_cares.shear_frequency)

    def test_invalid_ong_identify(self):
        """
        O pet tem que ser da ong que irá edita-lo.
        """

        request = GenericTestUtils.authenticate(self.petguard_partner1.account)

        variables = {
            'identify': self.pet1.id,
            'data': {'special_cares': {'shear_frequency': 2}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Não foi encontrado o pet com o identificador passado.",
                "cause": f"ID: {self.pet1.id}"
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables,
            context=request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(0, self.pet1.special_cares.shear_frequency)

    def test_invalid_not_owner_pet_identify(self):
        """
        O pet tem que ser do usuário que irá edita-lo.
        """

        variables = {
            'identify': self.pet2.id,
            'data': {'special_cares': {'shear_frequency': 2}}
        }

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
            variables=variables,
            context=self.request
        )

        self.pet1.refresh_from_db()
        self.assertEqual(0, self.pet1.special_cares.shear_frequency)

    def test_invalid_not_owner_ong_pet_identify(self):
        """
        O pet tem que ser da ong que irá edita-lo.
        """

        variables = {
            'identify': self.pet4.id,
            'data': {'special_cares': {'shear_frequency': 2}}
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
            variables=variables,
            context=self.request
        )

        self.pet4.refresh_from_db()
        self.assertEqual(0, self.pet4.special_cares.shear_frequency)

    def test_not_logged_user(self):
        """
        Usuário não logado não pode atualizar pet.
        """

        variables = {
            'identify': self.pet1.id,
            'data': {'special_cares': {'shear_frequency': 2}}
        }

        result = {
            "status": 400,
            "error": {
                "message": "Usuário precisa está autenticado para realizar essa ação.",
                "cause": "Usuário não está autenticado no sistema."
            }
        }

        GenericTestUtils.execute_graphql(
            test=self,
            query=self.query,
            data=result,
            variables=variables
        )

        self.pet1.refresh_from_db()
        self.assertEqual(0, self.pet1.special_cares.shear_frequency)
