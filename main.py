from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = '12345'  # Замените на свой секретный ключ

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

UPLOAD_FOLDER = 'audio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Предположим, у вас есть список карточек с словами и переводами
flashcards = [
    {"word": "Apple", "translation": "Яблоко", "image": "apple.jpg"},
    {"word": "Car", "translation": "Машина", "image": "car.jpg"},
    {"word": "Lion", "translation": "Лев", "image": "lion.jpg"},
    {"word": "Chair", "translation": "Стул", "image": "chair.png"},
    {"word": "Book", "translation": "Книга", "image": "book.jpg"},
]

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    user = User(request.form['username'])
    login_user(user)
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', flashcards=flashcards)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File {filename} uploaded successfully'
    return 'No file uploaded'

@app.route('/play_audio/<filename>')
@login_required
def play_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/test')
@login_required
def test():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True)
