{{cookiecutter.content}}

{% if cookiecutter.teste %}
print("Passei no teste")
{% else %}
    print("Não passei no teste")
{% endif%}

{% for i in cookiecutter.loop %}
print(i)
{% endfor %}

{% for i in cookiecutter.empty %}
print(i)
{% empty %}
print("Vazio")
{% endfor %}

{% for extension, detail in cookiecutter.dict | dictsort %}
    print("{{extension}}")
    print("{{detail.oii}}")
{% endfor %}