{% set objects = ["Pig", "Dog", "Biltong"] %}
{% set methods = ["bite", "snarl", "kill"] %}
{% for object in objects %}
    class {{ object }}:
        def __init__(self):
            pass

        {% for method in methods %}
            def {{ method }}(self):
                print("The Beast does {}!".format('{{ method }}'))

        {% endfor %}


{% endfor %}
