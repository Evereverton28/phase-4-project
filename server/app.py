from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_cors import CORS
from models import db, User, Doctor, Patient, Symptom, patient_symptom  # Import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Required for session management

db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
CORS(app)  # Enable CORS

login_manager = LoginManager(app)

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
    if user and user.check_password(password):
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
    
    new_user = User(username=username)
    new_user.set_password(password)
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
