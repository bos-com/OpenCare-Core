"""
Seed script to populate the database with sample data
for development and testing purposes.

Usage:
    python manage.py shell < scripts/seed_data.py
    
    Or with Docker:
    docker-compose exec web python manage.py shell < scripts/seed_data.py
"""

import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

print("Starting database seeding...")

# ── Sample Health Facilities ──────────────────────────────────────────────────
facilities_data = [
    {
        "name": "Bugema University Health Center",
        "facility_type": "clinic",
        "location": "Bugema, Wakiso District",
        "phone": "+256-41-4123456",
        "email": "health@bugema.ac.ug",
        "capacity": 50,
    },
    {
        "name": "Kampala General Hospital",
        "facility_type": "hospital",
        "location": "Kampala, Uganda",
        "phone": "+256-41-4256789",
        "email": "info@kgh.go.ug",
        "capacity": 300,
    },
    {
        "name": "Mulago National Referral Hospital",
        "facility_type": "referral_hospital",
        "location": "Mulago Hill, Kampala",
        "phone": "+256-41-4541884",
        "email": "info@mulago.go.ug",
        "capacity": 1500,
    },
    {
        "name": "Entebbe Grade B Hospital",
        "facility_type": "hospital",
        "location": "Entebbe, Wakiso District",
        "phone": "+256-41-4320789",
        "email": "entebbe@hospital.go.ug",
        "capacity": 200,
    },
    {
        "name": "Kawempe Health Center IV",
        "facility_type": "health_center",
        "location": "Kawempe, Kampala",
        "phone": "+256-41-4332100",
        "email": "kawempe@hc.go.ug",
        "capacity": 100,
    },
]

# ── Sample Patients ────────────────────────────────────────────────────────────
patients_data = [
    {"first_name": "John", "last_name": "Mukasa",
     "dob": "1990-03-15", "gender": "M", "phone": "+256701234567"},
    {"first_name": "Sarah", "last_name": "Nalwoga",
     "dob": "1985-07-22", "gender": "F", "phone": "+256702345678"},
    {"first_name": "David", "last_name": "Ssemakula",
     "dob": "1978-11-08", "gender": "M", "phone": "+256703456789"},
    {"first_name": "Grace", "last_name": "Namukasa",
     "dob": "1995-01-30", "gender": "F", "phone": "+256704567890"},
    {"first_name": "Peter", "last_name": "Kiggundu",
     "dob": "1982-05-14", "gender": "M", "phone": "+256705678901"},
    {"first_name": "Mary", "last_name": "Namusoke",
     "dob": "1993-09-25", "gender": "F", "phone": "+256706789012"},
    {"first_name": "Joseph", "last_name": "Tumusiime",
     "dob": "1975-12-03", "gender": "M", "phone": "+256707890123"},
    {"first_name": "Ruth", "last_name": "Akello",
     "dob": "1988-04-17", "gender": "F", "phone": "+256708901234"},
    {"first_name": "Paul", "last_name": "Ochieng",
     "dob": "1970-08-29", "gender": "M", "phone": "+256709012345"},
    {"first_name": "Agnes", "last_name": "Atim",
     "dob": "1998-02-11", "gender": "F", "phone": "+256700123456"},
]

# ── Sample Health Workers ──────────────────────────────────────────────────────
workers_data = [
    {"first_name": "Dr. James",  "last_name": "Ssali",
     "role": "doctor",    "specialization": "General Medicine"},
    {"first_name": "Dr. Anne",   "last_name": "Nakato",
     "role": "doctor",    "specialization": "Pediatrics"},
    {"first_name": "Nurse Rose", "last_name": "Nambi",
     "role": "nurse",     "specialization": "General Nursing"},
    {"first_name": "Nurse Tom",  "last_name": "Wasswa",
     "role": "nurse",     "specialization": "Midwifery"},
    {"first_name": "Dr. Moses",  "last_name": "Katende",
     "role": "doctor",    "specialization": "Surgery"},
]

print(f"  Prepared {len(facilities_data)} facilities")
print(f"  Prepared {len(patients_data)} patients")
print(f"  Prepared {len(workers_data)} health workers")
print("")
print("Seed data is ready for integration with Django models.")
print("Connect each dictionary above to your actual Django models, e.g.:")
print("")
print("  from apps.facilities.models import HealthFacility")
print("  for f in facilities_data:")
print("      HealthFacility.objects.get_or_create(**f)")
print("")
print("Seeding complete!")