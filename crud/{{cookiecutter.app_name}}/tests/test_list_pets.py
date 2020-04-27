from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from model_bakery import baker
from common.test_utils import GenericTestUtils
from petguard.users.models import PetGuardUser, PetGuardPartner
from petguard.users.models.petguard_user import insert_qrcode_to_account
from petguard.pets.models import Pet


User = get_user_model()


class ListPetsTestCase(TestCase):
    """
    Teste para listar os pets de um usuário no sistema
    """

    def setUp(self):
        """
        Método que roda a cada teste
        """

        post_save.disconnect(insert_qrcode_to_account, sender=PetGuardUser, dispatch_uid='insert_qrcode_to_account')

        user1 = User.objects.create_user(
            username='fulano01',
            name='Fulano 01',
            email='fulano01@gmail.com',
            password='django1234'
        )
        self.user1 = PetGuardUser.objects.create(account=user1)

        user2 = User.objects.create_user(
            username='fulano02',
            name='Fulano 02',
            email='fulano02@gmail.com',
            password='django1234'
        )
        self.user2 = PetGuardUser.objects.create(account=user2, plan="PAID")

        partner1 = User.objects.create_user(
            username='ong01',
            name='Ong 01',
            email='ong01@gmail.com',
            password='django1234'
        )
        self.partner1 = PetGuardPartner.objects.create(account=partner1)

        partner2 = User.objects.create_user(
            username='ong02',
            name='Ong 02',
            email='ong02@gmail.com',
            password='django1234'
        )
        self.partner2 = PetGuardPartner.objects.create(account=partner2)

        baker.make(Pet, _quantity=3, owner=self.user1, kind="DOG", name="XU")
        baker.make(Pet, _quantity=1, owner=self.user1, kind="DOG", name="PUFF")
        baker.make(Pet, _quantity=2, owner=self.user1, kind="CAT", name="TOFF")
        baker.make(Pet, _quantity=3, owner=self.user2, kind="DOG", name="REX")
        baker.make(Pet, _quantity=3, ong=self.partner1, kind="DOG", name="TEF")
        baker.make(Pet, _quantity=2, ong=self.partner1, kind="CAT", name="BUFF")
        baker.make(Pet, _quantity=1, ong=self.partner2, kind="DOG", name="XAA")
        baker.make(Pet, _quantity=1, ong=self.partner2, kind="CAT", name="XEE", is_adopted=True)

        self.query = """
            query QueryPets($id: String!, $is_adoption: Boolean, $search: String, $kind: String, $skip: Int, $first: Int) {
                petguard {
                    pets {
                        collection(identify: $id, is_adoption: $is_adoption, search: $search, kind: $kind, skip: $skip, first: $first) {
                            kind
                            name
                        }
                    }
                }
            }
        """

        self.variables = {
            "id": self.user1.account.email,
            "is_adoption": False
        }

        self.maxDiff = None

    def tearDown(self):
        """
        This method will run after any test.
        """

        Pet.objects.all().delete()
        PetGuardPartner.objects.all().delete()
        PetGuardUser.objects.all().delete()
        User.objects.all().delete()

    def test_list_owner1_pets(self):
        """
        Lista os pets do owner1 pegando seus atributos.
        """

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "PUFF"},
                            {"kind": "CAT", "name": "TOFF"},
                            {"kind": "CAT", "name": "TOFF"}
                        ]
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

    def test_list_owner2_pets(self):
        """
        Lista os pets do owner2 pegando seus atributos.
        """

        self.variables['id'] = self.user2.account.email

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "REX"},
                            {"kind": "DOG", "name": "REX"},
                            {"kind": "DOG", "name": "REX"}
                        ]
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

    def test_list_partner1_pets(self):
        """
        Lista os pets do partner1 pegando seus atributos.
        """

        self.variables['id'] = self.partner1.account.email

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "CAT", "name": "BUFF"},
                            {"kind": "CAT", "name": "BUFF"}
                        ]
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

    def test_list_partner2_pets(self):
        """
        Lista os pets do partner2 pegando seus atributos.
        """

        self.variables['id'] = self.partner2.account.email

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "XAA"},
                            {"kind": "CAT", "name": "XEE"}
                        ]
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

    def test_adoption_list_pets(self):
        """
        Lista os pets em adoção pegando seus atributos.
        """

        self.variables = {
            "id": self.user1.account.email,
            "is_adoption": True
        }

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "CAT", "name": "BUFF"},
                            {"kind": "CAT", "name": "BUFF"},
                            {"kind": "DOG", "name": "XAA"}
                        ]
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

    def test_list_pets_by_name(self):
        """
        Filtra os pets do owner1 pelo seu nome.
        """

        self.variables['search'] = "XU"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "XU"}
                        ]
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

    def test_list_ong_pets_by_name(self):
        """
        Filtra os pets do partner1 pelo seu nome.
        """

        self.variables['id'] = self.partner1.account.email
        self.variables['search'] = "BUFF"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "CAT", "name": "BUFF"},
                            {"kind": "CAT", "name": "BUFF"}
                        ]
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

    def test_list_adoption_pets_by_name(self):
        """
        Filtra os pets para adoção pelo seu nome.
        """

        self.variables['search'] = "Ong 01"
        self.variables['is_adoption'] = True

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "CAT", "name": "BUFF"},
                            {"kind": "CAT", "name": "BUFF"}
                        ]
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

    def test_list_pets_by_kind(self):
        """
        Filtra os pets do owner1 pelo seu tipo.
        """

        self.variables['kind'] = "CAT"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "CAT", "name": "TOFF"},
                            {"kind": "CAT", "name": "TOFF"}
                        ]
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

    def test_list_ong_pets_by_kind(self):
        """
        Filtra os pets do partner1 pelo seu tipo.
        """

        self.variables['id'] = self.partner1.account.email
        self.variables['kind'] = "DOG"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"},
                            {"kind": "DOG", "name": "TEF"}
                        ]
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

    def test_list_adoption_pets_by_kind(self):
        """
        Filtra os pets para adoção pelo seu tipo.
        """

        self.variables['kind'] = "CAT"
        self.variables['is_adoption'] = True

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "CAT", "name": "BUFF"},
                            {"kind": "CAT", "name": "BUFF"}
                        ]
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

    def test_list_pets_by_kind_and_name(self):
        """
        Filtra os pets do owner1 pelo seu tipo e nome.
        """

        self.variables['kind'] = "DOG"
        self.variables['search'] = "PUFF"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "PUFF"}
                        ]
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

    def test_list_pets_by_kind_and_name_empty_result(self):
        """
        Filtra os pets do owner1 pelo seu tipo e nome sem resultados.
        """

        self.variables['kind'] = "CAT"
        self.variables['search'] = "XU"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": []
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

    def test_list_pets_pagination1(self):
        """
        Paginar os pets (Página 01).
        """

        self.variables['first'] = 2
        self.variables['skip'] = 0

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "XU"}
                        ]
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

    def test_list_pets_pagination2(self):
        """
        Paginar os pets (página 02).
        """

        self.variables['first'] = 2
        self.variables['skip'] = 2

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "PUFF"}
                        ]
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

    def test_list_pets_pagination3(self):
        """
        Paginar os pets (página 03).
        """

        self.variables['first'] = 2
        self.variables['skip'] = 4

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "CAT", "name": "TOFF"},
                            {"kind": "CAT", "name": "TOFF"}
                        ]
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

    def test_list_pets_pagination_with_filter1(self):
        """
        Paginar os pets com filtro.
        """

        self.variables['first'] = 2
        self.variables['skip'] = 0
        self.variables['search'] = "PUFF"
        self.variables['kind'] = "DOG"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "PUFF"},
                        ]
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

    def test_list_pets_pagination_with_filter2(self):
        """
        Paginar os pets com filtro.
        """

        self.variables['first'] = 2
        self.variables['skip'] = 0
        self.variables['search'] = "XU"
        self.variables['kind'] = "DOG"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": [
                            {"kind": "DOG", "name": "XU"},
                            {"kind": "DOG", "name": "XU"}
                        ]
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

    def test_list_pets_pagination_with_filter3(self):
        """
        Paginar os pets com filtro.
        """

        self.variables['first'] = 2
        self.variables['skip'] = 0
        self.variables['search'] = "XU"
        self.variables['kind'] = "CAT"

        result = {
            "status": 200,
            "data": {
                "petguard": {
                    "pets": {
                        "collection": []
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
