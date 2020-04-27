from django.db import models
from common.exceptions import CustomError
from common.models import BaseModel
{% for obj in cookiecutter.model.imports -%}
from {{obj.path}} import {% for class_obj in obj.value %}{{class_obj}}{{", " if not loop.last }}{% endfor %}
{% endfor %}

class {{cookiecutter.model.name}}Manager(models.Manager):
    """
    Gerenciado de querysets.
    """

    def get_{{cookiecutter.model.file|lower}}(self, identify):
        """
        Pega o objeto relacionada a modelo.
        """

        try:
            obj = self.model.objects.get(id=identify)
        except {{cookiecutter.model.name}}.DoesNotExist:
            raise CustomError(
                message="Não foi encontrado o {{cookiecutter.model.file|lower|replace('_', ' ')}} com o identificador passado.",
                cause=f"ID: {identify}"
            )

        return obj


class {{cookiecutter.model.name}}(BaseModel):
    """
    {{cookiecutter.model.description}}
    """

    {% for field in cookiecutter.model.fields -%}
    {{field.name}} = models.{{field.type}}(
        {% if field.type in ["ForeignKey", "OneToOneField", "ManyToManyField"] -%}
        {{field.relationship}},
        {%- elif field.type == "ImageField" -%}
        upload_to="{{field.upload_to}}",
        {%- else -%}
        "{{field.title}}",
        {%- endif %}
        help_text="{{field.description}}",
        {%- for key, value in field.attr.items() %}
        {{key}}={{value}}{{"," if not loop.last }}
        {%- endfor %}
    )

    {% endfor -%}

    objects = {{cookiecutter.model.name}}Manager()

    def __str__(self):
        """
        Retorno o objeto em formato de string.
        """

        return self.{{cookiecutter.model.string_attr}}

    class Meta:
        """
        Algumas informações adicionais.
        """

        db_table = "{{cookiecutter.model.db_name}}"
        ordering = {{cookiecutter.model.ordering}}
