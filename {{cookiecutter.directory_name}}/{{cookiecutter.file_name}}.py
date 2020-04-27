{{cookiecutter.content}}

print("{{cookiecutter.mydict['oii']}}")

{% if cookiecutter.teste %}
print("Passei no teste")
{% elif cookiecutter.content == "oii" %}
print("Ola do python")
{% else %}
    print("Não passei no teste")
{% endif%}

{% for i in cookiecutter.loop %}
print(i)
{% endfor %}


{% for i in cookiecutter.empty %}
print(i)
{% else %}
print("Vazio")
{% endfor %}
