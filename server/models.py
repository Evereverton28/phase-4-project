# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialty = db.Column(db.String(150), nullable=False)
    patients = db.relationship('Patient', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    symptoms = db.relationship('Symptom', secondary='patient_symptom', backref='patients')
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

# Association table for patient symptoms
patient_symptom = db.Table('patient_symptom',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True),
    db.Column('symptom_id', db.Integer, db.ForeignKey('symptom.id'), primary_key=True),
    db.Column('diagnosis', db.String(100))
)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=False)

# CRUD Methods
def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def create_doctor(name, specialty):
    doctor = Doctor(name=name, specialty=specialty)
    db.session.add(doctor)
    db.session.commit()
    return doctor

def create_patient(name, age, doctor_id):
    patient = Patient(name=name, age=age, doctor_id=doctor_id)
    db.session.add(patient)
    db.session.commit()
    return patient

def create_symptom(name, description):
    symptom = Symptom(name=name, description=description)
    db.session.add(symptom)
    db.session.commit()
    return symptom

def add_symptom_to_patient(patient_id, symptom_id, diagnosis):
    stmt = patient_symptom.insert().values(patient_id=patient_id, symptom_id=symptom_id, diagnosis=diagnosis)
    db.session.execute(stmt)
    db.session.commit()

def create_appointment(patient_id, doctor_id, date, time, reason):
    appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, reason=reason)
    db.session.add(appointment)
    db.session.commit()
    return appointment

def update_user(user_id, username=None, password=None):
    user = User.query.get(user_id)
    if not user:
        return None
    if username:
        user.username = username
    if password:
        user.set_password(password)
    db.session.commit()
    return user

def update_doctor(doctor_id, name=None, specialty=None):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return None
    if name:
        doctor.name = name
    if specialty:
        doctor.specialty = specialty
    db.session.commit()
    return doctor

def update_patient(patient_id, name=None, age=None, doctor_id=None):
    patient = Patient.query.get(patient_id)
    if not patient:
        return None
    if name:
        patient.name = name
    if age:
        patient.age = age
    if doctor_id:
        patient.doctor_id = doctor_id
    db.session.commit()
    return patient

def update_symptom(symptom_id, name=None, description=None):
    symptom = Symptom.query.get(symptom_id)
    if not symptom:
        return None
    if name:
        symptom.name = name
    if description:
        symptom.description = description
    db.session.commit()
    return symptom

def update_appointment(appointment_id, patient_id=None, doctor_id=None, date=None, time=None, reason=None):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return None
    if patient_id:
        appointment.patient_id = patient_id
    if doctor_id:
        appointment.doctor_id = doctor_id
    if date:
        appointment.date = date
    if time:
        appointment.time = time
    if reason:
        appointment.reason = reason
    db.session.commit()
    return appointment

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
    return doctor

def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return patient

def delete_symptom(symptom_id):
    symptom = Symptom.query.get(symptom_id)
    if symptom:
        db.session.delete(symptom)
        db.session.commit()
    return symptom

def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
    return appointment
