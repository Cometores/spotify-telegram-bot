from jinja2 import Template
''' Работа с макросами '''

html = '''
{%- macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{ value | e }}" size="{{ size }}">
{%- endmacro%}

<p>{{ input('username') }}
<p>{{ input('email') }}
<p>{{ input('password') }}
'''

tm = Template(html)
msg = tm.render()
print(msg)



''' Вложенные макросы '''
persons = [
    {"name": "Алексей", "old": 18, "weight": 78.6},
    {"name": "Николай", "old": 28, "weight": 82.3},
    {"name": "Иван", "old": 33, "weight": 94.0}
]

html = '''
{% macro list_users(u_param) -%}
<ul>
{% for u in u_param -%}
    <li>{{u.name}} {{caller(u)}}
{%- endfor %}
</ul>
{%- endmacro %}

{% call(user) list_users(users) %}
    <ul>
    <li>age: {{ user.old }}
    <li>weight: {{ user.weight }}
    </ul>
{% endcall -%}
'''

tm = Template(html)
msg = tm.render(users=persons)
print(msg)