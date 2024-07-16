#!/usr/bin/env python3

from app import app
from models import db, Doctor, Patient, Symptom, User

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Adding sample data for doctors
        doctor1 = Doctor(name='Dr. John Doe', specialty='Cardiology')
        doctor2 = Doctor(name='Dr. Jane Smith', specialty='Neurology')

        # Adding sample data for patients
        patient1 = Patient(name='Alice Johnson', age=30, doctor=doctor1)
        patient2 = Patient(name='Bob Brown', age=45, doctor=doctor2)

        # Adding sample data for symptoms
        symptom1 = Symptom(name='Headache', description='Pain in head')
        symptom2 = Symptom(name='Nausea', description='Feeling of sickness with an inclination to vomit')

        # Associating patients with symptoms
        patient1.symptoms.append(symptom1)
        patient2.symptoms.append(symptom2)

        # Adding sample data for users with plain text passwords
        user1 = User(username='user1', password='password1')
        user2 = User(username='user2', password='password2')

        db.session.add_all([doctor1, doctor2, patient1, patient2, symptom1, symptom2, user1, user2])
        db.session.commit()
        print("Data seeded successfully!")

if __name__ == "__main__":
    seed_data()
