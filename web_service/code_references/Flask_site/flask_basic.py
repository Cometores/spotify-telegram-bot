from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adflfadfhieuhk2134hkjaf'

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route("/index")
@app.route("/")
def index():
    print(url_for('index'))
    return render_template("index.html", menu=menu)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template("about.html", title="About", menu=menu)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
        print(request.form['username'])

    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu), 404
    #404 чтобы возвращать правильную ошибку


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'cometores' and request.form['psw'] == "123":
        session['userLogged'] = request.form["username"]
        return redirect(url_for('profile', username=session['userLogged']))

    return  render_template('login.html', title='Авторизация', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Профиль пользователя: {username}"


''' Переменные адреса '''
@app.route("/profile2/<path:username>") # profile/user/123 -> user/123
def profile2(username):
    return f"Пользователь: {username}"

@app.route("/numbers/<int:nums>") #Если ввести не цифры -> Страница не будет найдена
def numbers(nums):
    return f"Введеные цифры: {nums}"


''' Создание тестового контекста запроса '''
with app.test_request_context():
    print(url_for('about'))
    print(url_for('profile', username="admin"))


''' Запуск приложения '''
if __name__ == "__main__":
    app.run(debug=True)