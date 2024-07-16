from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Required for session management

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

login_manager = LoginManager(app)

# ORM Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    patients = db.relationship('Patient', backref='doctor', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    symptoms = db.relationship('Symptom', secondary='patient_symptom', backref='patients')

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

# Association table for patient symptoms
patient_symptom = db.Table('patient_symptom',
                           db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
                           db.Column('symptom_id', db.Integer, db.ForeignKey('symptom.id')),
                           db.Column('diagnosis', db.String(100))
                           )

# Login Manager setup
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': 'This is a protected resource'})

# List of Symptoms
@app.route('/symptoms', methods=['GET'])
def list_symptoms():
    symptoms = Symptom.query.all()
    symptoms_list = [{'id': symptom.id, 'name': symptom.name, 'description': symptom.description} for symptom in symptoms]
    return jsonify(symptoms_list)

# List of Doctors
@app.route('/doctors', methods=['GET'])
def list_doctors():
    doctors = Doctor.query.all()
    doctors_list = [{'id': doctor.id, 'name': doctor.name, 'specialty': doctor.specialty} for doctor in doctors]
    return jsonify(doctors_list)

# List of Users
@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_list)

if __name__ == '__main__':
    app.run(debug=True)
