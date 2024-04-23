from flask import Flask, redirect, render_template, abort, request
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms.user import RegisterForm, LoginForm
from data import db_session
from data.users import User
from data.adds import Adds
from forms.adds import AddsForm
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    adds = db_sess.query(Adds).filter()
    return render_template("index.html", adds=adds)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile')
@login_required
def profile():
    db_sess = db_session.create_session()
    adds = db_sess.query(Adds).filter(Adds.user == current_user)
    return render_template("profile.html", adds=adds)


@app.route('/lost',  methods=['GET', 'POST'])
@login_required
def add_adds_lost():
    form = AddsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        adds = Adds()
        type_pet = []
        if form.type_cat.data:
            type_pet.append('кошка')
        if form.type_dog.data:
            type_pet.append('собака')
        if form.type_other.data:
            type_pet.append('другое')
        gender = []
        if form.gender_male:
            gender.append('мужской')
        if form.gender_female:
            gender.append('женский')
        adds.type_pet = ' '.join(type_pet)
        adds.gender = ' '.join(gender)
        adds.place = form.place.data
        adds.time = form.time.data
        adds.description = form.description.data
        adds.name = form.name.data
        adds.number = form.number.data
        adds.lost_find = 'потерян'
        current_user.adds.append(adds)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('lost.html', title='Добавление объявления',
                           form=form)


@app.route('/find',  methods=['GET', 'POST'])
@login_required
def add_adds_find():
    form = AddsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        adds = Adds()
        type_pet = []
        if form.type_cat.data:
            type_pet.append('кошка')
        if form.type_dog.data:
            type_pet.append('собака')
        if form.type_other.data:
            type_pet.append('другое')
        gender = []
        if form.gender_male:
            gender.append('мужской')
        if form.gender_female:
            gender.append('женский')
        adds.type_pet = ' '.join(type_pet)
        adds.gender = ' '.join(gender)
        adds.place = form.place.data
        adds.time = form.time.data
        adds.description = form.description.data
        adds.name = form.name.data
        adds.number = form.number.data
        adds.lost_find = 'найден'
        current_user.adds.append(adds)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('find.html', title='Добавление объявления',
                               form=form)


@app.route('/adds/<int:id>')
def more_details(id):
    db_sess = db_session.create_session()
    adds = db_sess.query(Adds).get(id)
    return render_template('more_details.html', title='Подробная информация', adds=adds)


@app.route('/adds_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    adds = db_sess.query(Adds).filter(Adds.id == id,
                                      Adds.user == current_user
                                      ).first()
    if adds:
        db_sess.delete(adds)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1', debug=True)
