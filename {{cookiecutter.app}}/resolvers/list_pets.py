from petguard.pets.models import Pet
from django.db.models import Q


class ListPetResolver:
    """
    Classe responsável pela lógica de listar pets
    """

    def __init__(self, identify, kwargs):
        """
        Construtor
        """

        self.is_adoption = kwargs.get('is_adoption')

        if self.is_adoption:
            self.query = Pet.objects.filter(Q(owner=None), ~Q(ong=None), is_adopted=False)
        else:
            self.query = Pet.objects.filter(
                Q(owner__account__email=identify) |
                Q(owner__account__username=identify) |
                Q(ong__account__email=identify) |
                Q(ong__account__username=identify)
            )

        self.search = kwargs.get('search')
        self.kind = kwargs.get('kind')
        self.is_adopted = kwargs.get('is_adopted')
        self.skip = kwargs.get('skip')
        self.first = kwargs.get('first')

    def __apply_search(self):
        """
        Aplica o filtro de pesquisa.
        """

        if self.search:
            self.query = self.query.filter(
                Q(name__icontains=self.search) |
                Q(ong__account__name=self.search) |
                Q(ong__account__email=self.search) |
                Q(ong__cnpj=self.search)
            )

    def __apply_kind_filter(self):
        """
        Aplica o filtro de tipos de pet.
        """

        if self.kind:
            self.query = self.query.filter(kind=self.kind)

    def __apply_adopted(self):
        """
        Aplica o filtro de pets adotados.
        """

        if self.is_adopted is not None:
            self.query = self.query.filter(is_adopted=self.is_adopted)

    def __apply_skip(self):
        """
        Aplica o filtro de pular N primeiros dados.
        """

        if self.skip:
            self.query = self.query[self.skip:]

    def __apply_first(self):
        """
        Aplica filtro de pegar os N primeiros dados.
        """

        if self.first:
            self.query = self.query[:self.first]

    def get_result(self):
        """
        Resultado do resolver.
        """

        self.__apply_search()
        self.__apply_kind_filter()
        self.__apply_adopted()
        self.__apply_skip()
        self.__apply_first()

        return self.query
