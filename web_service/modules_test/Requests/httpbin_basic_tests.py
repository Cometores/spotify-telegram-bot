import requests

r = requests.get('https://httpbin.org/')
#print(dir(r)) - имена всех возможных атрибутов и методов класса Response
#print(help(r)) - все возможные атрибуты и методы с их описанием
#print(r.text) - HTML страница
#print(r.status_code) - статус ответа
#print(r.ok) - True для всего что меньше 400
#print(r.url) - Пишет url для запроса с параметрами

'''Работа с изображениями'''
payload = {'accept': 'image/jpeg'}
r = requests.get('https://httpbin.org/image/png')

with open('img.png', 'wb') as f:
    f.write(r.content)


'''Работа с аутентификацией'''
r = requests.get('https://httpbin.org/basic-auth/and/test', auth=('and', 'test'))
print(r.text)

