# import hashlib
# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Xre.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'your_secret_key'
# db = SQLAlchemy(app)
#
# # Определение моделей
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)  # Поле для пароля
#     messages = db.relationship('Message', backref='sender', foreign_keys='Message.user_id', lazy=True)
#
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
# with app.app_context():
#     db.create_all()
#
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()  # Хеширование пароля
#
# def check_password(hashed_password, user_password):
#     return hashed_password == hashlib.sha256(user_password.encode()).hexdigest()  # Проверка пароля
#
# @app.route('/')
# def index():
#     return render_template('login.html')
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         # Проверка на существование имени пользователя
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             return render_template('register.html', error="Username already exists. Please choose a different one.")
#
#         hashed_password = hash_password(password)  # Хеширование пароля
#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#
#     return render_template('register.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password(user.password, password):  # Проверка пароля
#             session['user_id'] = user.id
#             return redirect(url_for('wall'))
#     return render_template('login.html')
#
# @app.route('/wall', methods=['GET', 'POST'])
# def wall():
#     if request.method == 'POST':
#         content = request.form['content']
#         user_id = session.get('user_id')
#         if user_id and content:
#             new_message = Message(content=content, user_id=user_id, recipient_id=user_id)  # recipient_id можно изменить по необходимости
#             db.session.add(new_message)
#             db.session.commit()
#             return redirect(url_for('wall'))
#
#     messages = Message.query.all()  # Получаем все сообщения
#     return render_template('wall.html', messages=messages)
#
# @app.route('/send_message', methods=['POST'])
# def send_message():
#     content = request.form['content']
#     user_id = session.get('user_id')
#     if user_id and content:
#         new_message = Message(content=content, user_id=user_id, recipient_id=user_id)  # recipient_id можно изменить по необходимости
#         db.session.add(new_message)
#         db.session.commit()
#     return redirect(url_for('wall'))
#
#
# if __name__ == '__main__':
#     app.run(debug=True)





import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Xre.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Определение моделей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Поле для пароля
    messages = db.relationship('Message', backref='sender', foreign_keys='Message.user_id', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Поле для времени отправления

with app.app_context():
    db.create_all()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Хеширование пароля

def check_password(hashed_password, user_password):
    return hashed_password == hashlib.sha256(user_password.encode()).hexdigest()  # Проверка пароля

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка на существование имени пользователя
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error="Username already exists. Please choose a different one.")

        hashed_password = hash_password(password)  # Хеширование пароля
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password(user.password, password):  # Проверка пароля
            session['user_id'] = user.id
            return redirect(url_for('wall'))
        else:
            flash("Invalid username or password")  # Сообщение об ошибке

    return render_template('login.html')

@app.route('/wall', methods=['GET', 'POST'])
def wall():
    if request.method == 'POST':
        content = request.form['content']
        user_id = session.get('user_id')
        if user_id and content:
            new_message = Message(content=content, user_id=user_id, recipient_id=user_id)  # timestamp будет установлен автоматически
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('wall'))

    messages = Message.query.all()  # Получаем все сообщения
    return render_template('wall.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.form['content']
    user_id = session.get('user_id')
    if user_id and content:
        new_message = Message(content=content, user_id=user_id, recipient_id=user_id)  # timestamp будет установлен автоматически
        db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('wall'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Удаляем пользователя из сессии
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)