from http.client import TEMPORARY_REDIRECT

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    hash_and_salted_password = generate_password_hash(
        request.form.get('password'),
        method="pbkdf2:sha256",
        salt_length=8
    )
    user = User()
    user.name = request.form.get('name')
    user.email = request.form.get('email')
    user.password = hash_and_salted_password
    # user.password = request.form.get('password')

    if request.form:
        db.session.add(user)
        db.session.commit()

        '''
        51 Line Info
        code=302 Default , code=307 값을 줘야 name 값을 가져 오는 이유는?
        302는 기존 Method 와 Body 를 버리고 GET 방식으로 요청하는 반면,
        307 은 받은 요청 Method 와 Body 를 유지한채로 재 요청 하기 때문에,
        담겨 있던 name 이 정상적으로 secrets 페이지에 정상 적으로 출력.
        '''
        return redirect(url_for("secrets"), TEMPORARY_REDIRECT)
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets', methods=['GET', "POST"])
def secrets():
    return render_template("secrets.html", name=request.form.get('name'))


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    pass


if __name__ == "__main__":
    app.run(debug=True)
