from jinja2 import Environment, FileSystemLoader

''' Include Import '''

persons = [
    {"name": "Алексей", "old": 18, "weight": 78.6},
    {"name": "Николай", "old": 28, "weight": 82.3},
    {"name": "Иван", "old": 33, "weight": 94.0}
]

file_loader = FileSystemLoader("templates/separated")
env = Environment(loader=file_loader)

tm = env.get_template("page.html")
msg = tm.render(domain="http://abc.com", title="Jinja")

print(msg)