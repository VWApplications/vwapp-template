{{cookiecutter.content}}
{{cookiecutter.dict['zip_code']}}
{% if cookiecutter.active == "true" %}
print("Passei no teste")
{% elif cookiecutter.content == "oii" %}
print("Ola do python")
{% else %}
print("Não passei no teste")
{% endif%}
{% for fruit in cookiecutter.dict['fruits'] %}
print({{fruit}})
{% endfor %}