from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///obs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MODELLER
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='student')  # 'teacher' veya 'student' olabilir

    courses = db.relationship('Course', backref='user', lazy=True)
    notes = db.relationship('Note', backref='user', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Öğretmen ID'si

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    course = db.relationship('Course', backref='notes', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ROTALAR

@app.route('/')
def home():
    return render_template('anasayfa.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'student')

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Bu kullanıcı adı zaten mevcut.")

        hashed_password = generate_password_hash(password)
        new_user = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=hashed_password,
            role=role
        )
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
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Hatalı kullanıcı adı veya şifre.")
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.firstname)

@app.route('/derslerim')
@login_required
def derslerim():
    courses = Course.query.filter_by(user_id=current_user.id).all()
    return render_template('derslerim.html', courses=courses)
   

@app.route('/notlar')
@login_required
def notlar():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notlar.html', notes=notes)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/ders_ekle', methods=['GET', 'POST'])
@login_required
def ders_ekle():
    if request.method == 'POST':
        course_name = request.form['course_name']
        teacher_id = request.form['teacher_id']  # Kullanıcının seçtiği öğretmen ID'si
        
        if not course_name or not teacher_id:
            return render_template('ders_ekle.html', error="Ders adı ve öğretmen seçimi zorunludur.")
        
        new_course = Course(name=course_name, user_id=teacher_id)  # Öğretmen ID'si ile ilişkilendir
        db.session.add(new_course)
        db.session.commit()
        
        return render_template('ders_ekle.html', success="Ders başarıyla eklendi.")
    
    teachers = User.query.filter_by(role='teacher').all()  # Sadece öğretmenleri al
    return render_template('ders_ekle.html', teachers=teachers)




@app.route('/ders_guncelle/<int:course_id>', methods=['GET', 'POST'])
@login_required
def ders_guncelle(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        course_name = request.form['course_name']
        if not course_name:
            return render_template('ders_guncelle.html', course=course, error="Ders adı boş olamaz.")
        course.name = course_name
        db.session.commit()
        return redirect(url_for('derslerim'))
    return render_template('ders_guncelle.html', course=course)

@app.route('/ders_sil/<int:course_id>', methods=['POST'])
@login_required
def ders_sil(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('derslerim'))

@app.route('/not_ekle', methods=['GET', 'POST'])
@login_required
def not_ekle():
    if request.method == 'POST':
        grade = request.form['grade']
        course_id = request.form['course_id']
        if not grade or not course_id:
            return render_template('not_ekle.html', error="Not ve ders seçimi zorunludur.")
        new_note = Note(grade=grade, user_id=current_user.id, course_id=course_id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('notlar'))
    courses = Course.query.filter_by(user_id=current_user.id).all()
    return render_template('not_ekle.html', courses=courses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
