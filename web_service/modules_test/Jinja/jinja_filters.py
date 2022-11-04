from jinja2 import Template
''' Работа с фильтрами '''

# SUM
cars = [
    {'model': 'Audi', 'price': 23000},
    {'model': 'Skoda', 'price': 17300},
    {'model': 'Volvo', 'price': 44300},
    {'model': 'WV', 'price': 21300}
]

tm = Template("Суммарная цена автомобилей {{ cs | sum(attribute='price') }}")
msg = tm.render(cs=cars)
print(msg)

digs = [1, 2, 3, 4, 5]
tm = Template("Сумма {{ cs | sum }}")
msg = tm.render(cs=digs)
print(msg)


# MAX
tm = Template("Самый дорогой автомобиль {{ (cs | max(attribute='price')).model }}")
msg = tm.render(cs=cars)
print(msg)


# REPLACE
tm = Template("Меняем буквы {{ cs[2].model | replace('o', '0')  }}")
msg = tm.render(cs=cars)
print(msg, '\n')


'''Блок фильтр'''
persons = [
    {"name": "Алексей", "old": 18, "weight": 78.6},
    {"name": "Николай", "old": 28, "weight": 82.3},
    {"name": "Иван", "old": 33, "weight": 94.0}
]

tpl = '''
{%- for u in users -%}
{% filter upper %}{{u.name}}{%endfilter %}
{% endfor -%}
'''

tm = Template(tpl)
msg = tm.render(users=persons)
print(msg)

