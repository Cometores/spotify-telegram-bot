from jinja2 import Environment, FileSystemLoader

subs = ["Математика", "Физика", "Информатика", "Русский"]

file_loader = FileSystemLoader('templates/extend')
env = Environment(loader=file_loader)

template = env.get_template('ex_about.html')

output = template.render(list_table=subs)
print((output))