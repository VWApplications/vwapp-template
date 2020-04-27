from cookiecutter.main import cookiecutter

cookiecutter(
    template='.',
    checkout="master",
    directory="crud",
    no_input=True,
    overwrite_if_exists=True,
    output_dir="..",
    # skip_if_file_exists=True,
    extra_context={
        "app_name": "pets",
        "model": {
            "file": "pet",
            "name": "Pet",
            "description": "Animal de estimação.",
            "string_attr": "name",
            "db_name": "petguard_pets",
            "ordering": "('created_at',)",
            "imports": [
                {"path": "petguard.users.models", "value": ["PetGuardUser", "PetGuardPartner"]},
                {"path": ".alimentation", "value": ["Alimentation"]},
                {"path": ".special_cares", "value": ["SpecialCares"]}
            ],
            "fields": [
                {
                    "name": "owner",
                    "type": "ForeignKey",
                    "relationship": "PetGuardUser",
                    "description": "Dono do pet ou usuário que adotou o pet.",
                    "attr": {
                        "on_delete": "models.PROTECT",
                        "null": True
                    }
                },
                {
                    "name": "ong",
                    "type": "ForeignKey",
                    "relationship": "PetGuardPartner",
                    "description": "ONG responsável pelo pet.",
                    "attr": {
                        "on_delete": "models.PROTECT",
                        "related_name": "'pets'",
                        "null": True
                    }
                },
                {
                    "name": "alimentation",
                    "type": "OneToOneField",
                    "relationship": "Alimentation",
                    "description": "Alimentação do pet.",
                    "attr": {
                        "on_delete": "models.CASCADE",
                        "related_name": "'pet'",
                        "null": True
                    }
                },
                {
                    "name": "name",
                    "type": "CharField",
                    "title": "Nome do pet",
                    "description": "Nome do animal de estimação.",
                    "attr": {
                        "max_length": 30
                    }
                },
                {
                    "name": "breed",
                    "type": "CharField",
                    "title": "Raça do pet",
                    "description": "Raça do animal de estimação.",
                    "attr": {
                        "max_length": 20,
                        "blank": True
                    }
                },
                {
                    "name": "photo",
                    "type": "ImageField",
                    "upload_to": "'petguard_pets'",
                    "description": "Foto do animal de estimação.",
                    "attr": {
                        "verbose_name": "'Foto'",
                        "blank": True,
                        "null": True
                    }
                }
            ]
        }
    }
)