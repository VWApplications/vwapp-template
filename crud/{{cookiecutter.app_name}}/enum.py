from enum import Enum


class PetTypeEnum(Enum):
    """
    Tipos de animal de estimação
    """

    CAT = 'CAT'
    DOG = 'DOG'


class PetSexEnum(Enum):
    """
    Sexo do animal de estimação.
    """

    FEMALE = 'FEMALE'
    MALE = 'MALE'


class PetSizeEnum(Enum):
    """
    Porte do animal de estimação ou de outros dados.
    """

    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    BIG = 'BIG'


class PetTemperamentEnum(Enum):
    """
    Temperamentos do animal de estimação.
    """

    DOCILE = 'DOCILE'
    FRIENDLY = 'FRIENDLY'
    BRAVE = 'BRAVE'
