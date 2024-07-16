from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username

    def set_password(self, password):
        # Implement password hashing logic here
        self.password = password  # Replace with hashed password

    def check_password(self, password):
        # Implement password checking logic here
        return self.password == password  # Replace with password verification

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
