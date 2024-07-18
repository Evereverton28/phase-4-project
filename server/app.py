from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_cors import CORS
from models import db, User, Doctor, Patient, Symptom, Appointment, patient_symptom  # Import models

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

@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = [
        { 'id': 1, 'name': 'Dr. Faith Nyaboke', 'specialty': 'Cardiology', 'phone': '+254 123 456 789', 'email': 'faith.nyaboke@gmail.com', 'imageUrl': 'https://images.unsplash.com/photo-1651008376811-b90baee60c1f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8RG9jdG9yfGVufDB8fDB8fHww' },
        { 'id': 2, 'name': 'Dr. Jane Kinyua', 'specialty': 'Pediatrics', 'phone': '+254 234 567 890', 'email': 'jane.kinyua@example.com', 'imageUrl': 'https://images.unsplash.com/photo-1584467735815-f778f274e296?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8RG9jdG9yfGVufDB8fDB8fHww' },
        { 'id': 3, 'name': 'Dr. Michael Kimemia', 'specialty': 'Orthopedics', 'phone': '+254 345 678 901', 'email': 'michael.kimemia@icloud.com', 'imageUrl': 'https://images.unsplash.com/photo-1609743522471-83c84ce23e32?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fERvY3RvcnxlbnwwfHwwfHx8MA%3D%3D' },
        { 'id': 4, 'name': 'Dr. Gary Kimani', 'specialty': 'Dermatology', 'phone': '+254 456 789 012', 'email': 'gary.kimani@example.com', 'imageUrl': 'https://media.istockphoto.com/id/1486172842/photo/portrait-of-male-nurse-in-his-office.webp?b=1&s=170667a&w=0&k=20&c=X4TGvYkgE0Hqqdwv13z47msgfNAFLH9udGXPzWHlT9A=' },
        { 'id': 5, 'name': 'Dr. David', 'specialty': 'Neurology', 'phone': '+254 567 890 123', 'email': 'david.lee@example.com', 'imageUrl': 'https://images.unsplash.com/photo-1579684453401-966b11832744?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzV8fERvY3RvcnxlbnwwfHwwfHx8MA%3D%3D' },
    ]
    return jsonify(doctors)

# List of Symptoms
@app.route('/symptoms', methods=['GET'])
def list_symptoms():
    symptoms = Symptom.query.all()
    symptoms_list = [{'id': symptom.id, 'name': symptom.name, 'description': symptom.description} for symptom in symptoms]
    return jsonify(symptoms_list)

# List of Users
@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_list)

# Update User
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# Delete User
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.json
    name = data.get('name')
    specialty = data.get('specialty')

    new_doctor = Doctor(name=name, specialty=specialty)
    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor added successfully'}), 201

# Update Doctor
@app.route('/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404

    data = request.json
    if 'name' in data:
        doctor.name = data['name']
    if 'specialty' in data:
        doctor.specialty = data['specialty']

    db.session.commit()
    return jsonify({'message': 'Doctor updated successfully'})

# Delete Doctor
@app.route('/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'})

@app.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    doctor_id = data.get('doctor_id')

    new_patient = Patient(name=name, age=age, doctor_id=doctor_id)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient added successfully'}), 201


# Update Patient
@app.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    data = request.json
    if 'name' in data:
        patient.name = data['name']
    if 'age' in data:
        patient.age = data['age']
    if 'doctor_id' in data:
        patient.doctor_id = data['doctor_id']

    db.session.commit()
    return jsonify({'message': 'Patient updated successfully'})

# Delete Patient
@app.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully'})

# Update Symptom
@app.route('/symptoms/<int:id>', methods=['PUT'])
def update_symptom(id):
    symptom = Symptom.query.get(id)
    if not symptom:
        return jsonify({'message': 'Symptom not found'}), 404

    data = request.json
    if 'name' in data:
        symptom.name = data['name']
    if 'description' in data:
        symptom.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Symptom updated successfully'})

# Delete Symptom
@app.route('/symptoms/<int:id>', methods=['DELETE'])
def delete_symptom(id):
    symptom = Symptom.query.get(id)
    if not symptom:
        return jsonify({'message': 'Symptom not found'}), 404

    db.session.delete(symptom)
    db.session.commit()
    return jsonify({'message': 'Symptom deleted successfully'})

# Create Appointment
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    time = data.get('time')
    reason = data.get('reason')

    new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, reason=reason)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked successfully'}), 201

# Get Appointments
@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    appointments_list = [{
        'id': appointment.id,
        'patient_id': appointment.patient_id,
        'doctor_id': appointment.doctor_id,
        'date': appointment.date,
        'time': appointment.time,
        'reason': appointment.reason
    } for appointment in appointments]
    return jsonify(appointments_list)

# Update Appointment
@app.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404

    data = request.json
    if 'date' in data:
        appointment.date = data['date']
    if 'time' in data:
        appointment.time = data['time']
    if 'reason' in data:
        appointment.reason = data['reason']

    db.session.commit()
    return jsonify({'message': 'Appointment updated successfully'})

# Delete Appointment
@app.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
