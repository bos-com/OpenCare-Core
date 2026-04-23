"""
Management command to set up the OpenCare-Africa project with initial data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from apps.core.models import Location, HealthFacility, SystemConfiguration
from apps.patients.models import Patient
from apps.health_workers.models import HealthWorkerProfile
from apps.facilities.models import FacilityService
from apps.analytics.models import HealthMetrics
from apps.records.models import HealthRecord
import os
from datetime import date, datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up OpenCare-Africa project with initial data and configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-data',
            action='store_true',
            help='Skip creating sample data',
        )
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@opencare-africa.com',
            help='Admin user email address',
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='admin123',
            help='Admin user password',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up OpenCare-Africa project...')
        )

        # Create superuser if it doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            self.create_superuser(options['admin_email'], options['admin_password'])

        # Update site configuration
        self.update_site_config()

        # Create system configurations
        self.create_system_configs()

        if not options['skip_data']:
            # Create sample data
            self.create_sample_locations()
            self.create_sample_facilities()
            self.create_sample_services()
            self.create_sample_health_workers()
            self.create_sample_patients()
            self.create_sample_health_records()
            self.create_sample_analytics()

        self.stdout.write(
            self.style.SUCCESS('✅ OpenCare-Africa project setup completed successfully!')
        )

    def create_superuser(self, email, password):
        """Create a superuser account."""
        try:
            user = User.objects.create_superuser(
                username='admin',
                email=email,
                password=password,
                first_name='Admin',
                last_name='User',
                user_type='admin'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superuser created: {user.username}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Superuser creation failed: {e}')
            )

    def update_site_config(self):
        """Update Django site configuration."""
        try:
            site, created = Site.objects.get_or_create(
                id=1,
                defaults={
                    'domain': 'opencare-africa.com',
                    'name': 'OpenCare-Africa'
                }
            )
            if created:
                self.stdout.write('✅ Site configuration created')
            else:
                self.stdout.write('✅ Site configuration updated')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Site configuration failed: {e}')
            )

    def create_system_configs(self):
        """Create system configuration entries."""
        configs = [
            {
                'key': 'system_name',
                'value': 'OpenCare-Africa',
                'description': 'System name for display purposes',
                'is_public': True
            },
            {
                'key': 'system_version',
                'value': '1.0.0',
                'description': 'Current system version',
                'is_public': True
            },
            {
                'key': 'maintenance_mode',
                'value': 'false',
                'description': 'System maintenance mode flag',
                'is_public': False
            },
            {
                'key': 'max_file_size',
                'value': '10485760',
                'description': 'Maximum file upload size in bytes (10MB)',
                'is_public': True
            },
            {
                'key': 'session_timeout',
                'value': '3600',
                'description': 'Session timeout in seconds',
                'is_public': False
            }
        ]

        for config in configs:
            SystemConfiguration.objects.get_or_create(
                key=config['key'],
                defaults=config
            )
        
        self.stdout.write('✅ System configurations created')

    def create_sample_locations(self):
        """Create sample location hierarchy."""
        try:
            # Create country
            kenya, created = Location.objects.get_or_create(
                name='Kenya',
                defaults={
                    'location_type': 'country',
                    'latitude': -1.2921,
                    'longitude': 36.8219
                }
            )
            if created:
                self.stdout.write('✅ Sample country created: Kenya')

            # Create regions
            regions = [
                {
                    'name': 'Nairobi',
                    'location_type': 'region',
                    'parent': kenya,
                    'latitude': -1.2921,
                    'longitude': 36.8219
                },
                {
                    'name': 'Mombasa',
                    'location_type': 'region',
                    'parent': kenya,
                    'latitude': -4.0435,
                    'longitude': 39.6682
                },
                {
                    'name': 'Kisumu',
                    'location_type': 'region',
                    'parent': kenya,
                    'latitude': -0.1022,
                    'longitude': 34.7617
                }
            ]

            for region_data in regions:
                region, created = Location.objects.get_or_create(
                    name=region_data['name'],
                    parent=region_data['parent'],
                    defaults=region_data
                )
                if created:
                    self.stdout.write(f'✅ Sample region created: {region.name}')

            # Create districts
            nairobi = Location.objects.get(name='Nairobi', parent=kenya)
            districts = [
                {
                    'name': 'Nairobi County',
                    'location_type': 'district',
                    'parent': nairobi,
                    'latitude': -1.2921,
                    'longitude': 36.8219
                }
            ]

            for district_data in districts:
                district, created = Location.objects.get_or_create(
                    name=district_data['name'],
                    parent=district_data['parent'],
                    defaults=district_data
                )
                if created:
                    self.stdout.write(f'✅ Sample district created: {district.name}')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Sample locations creation failed: {e}')
            )

    def create_sample_facilities(self):
        """Create sample health facilities."""
        try:
            nairobi_county = Location.objects.get(name='Nairobi County')
            
            facilities = [
                {
                    'name': 'Kenyatta National Hospital',
                    'facility_type': 'hospital',
                    'location': nairobi_county,
                    'address': 'Hospital Road, Nairobi',
                    'phone_number': '+254-20-2726300',
                    'email': 'info@knh.or.ke',
                    'website': 'https://knh.or.ke',
                    'is_24_hours': True,
                    'contact_person_name': 'Dr. John Doe',
                    'contact_person_phone': '+254-700-000000',
                    'services_offered': ['emergency_care', 'surgery', 'maternity', 'pediatrics']
                },
                {
                    'name': 'Mama Lucy Kibaki Hospital',
                    'facility_type': 'hospital',
                    'location': nairobi_county,
                    'address': 'Kangundo Road, Nairobi',
                    'phone_number': '+254-20-1234567',
                    'email': 'info@mlkh.or.ke',
                    'website': '',
                    'is_24_hours': True,
                    'contact_person_name': 'Dr. Jane Smith',
                    'contact_person_phone': '+254-700-000001',
                    'services_offered': ['emergency_care', 'maternity', 'pediatrics']
                },
                {
                    'name': 'Nairobi West Hospital',
                    'facility_type': 'health_center',
                    'location': nairobi_county,
                    'address': 'Westlands, Nairobi',
                    'phone_number': '+254-20-9876543',
                    'email': 'info@nwh.or.ke',
                    'website': '',
                    'is_24_hours': False,
                    'contact_person_name': 'Dr. Robert Johnson',
                    'contact_person_phone': '+254-700-000002',
                    'services_offered': ['primary_care', 'laboratory', 'pharmacy']
                }
            ]

            for facility_data in facilities:
                facility, created = HealthFacility.objects.get_or_create(
                    name=facility_data['name'],
                    defaults=facility_data
                )
                if created:
                    self.stdout.write(f'✅ Sample facility created: {facility.name}')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Sample facilities creation failed: {e}')
            )

    def create_sample_services(self):
        """Create sample facility services."""
        try:
            facility = HealthFacility.objects.get(name='Kenyatta National Hospital')
            
            services = [
                {
                    'facility': facility,
                    'name': 'Emergency Care',
                    'category': 'emergency_care',
                    'description': '24/7 emergency medical services',
                    'is_available': True,
                    'cost': 5000.00,
                    'duration_minutes': 120
                },
                {
                    'facility': facility,
                    'name': 'General Surgery',
                    'category': 'specialized_care',
                    'description': 'Surgical procedures and consultations',
                    'is_available': True,
                    'cost': 15000.00,
                    'duration_minutes': 180
                },
                {
                    'facility': facility,
                    'name': 'Maternity Care',
                    'category': 'maternity',
                    'description': 'Prenatal, delivery, and postnatal care',
                    'is_available': True,
                    'cost': 8000.00,
                    'duration_minutes': 60
                }
            ]

            for service_data in services:
                service, created = FacilityService.objects.get_or_create(
                    facility=service_data['facility'],
                    name=service_data['name'],
                    defaults=service_data
                )
                if created:
                    self.stdout.write(f'✅ Sample service created: {service.name}')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Sample services creation failed: {e}')
            )

    def create_sample_health_workers(self):
        """Create sample health workers."""
        try:
            facility = HealthFacility.objects.get(name='Kenyatta National Hospital')
            
            # Create health worker users
            workers = [
                {
                    'username': 'dr.doe',
                    'email': 'john.doe@knh.or.ke',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'user_type': 'doctor',
                    'phone_number': '+254-700-000000',
                    'license_number': 'MED001',
                    'specialization': 'Emergency Medicine',
                    'years_of_experience': 8
                },
                {
                    'username': 'nurse.smith',
                    'email': 'jane.smith@knh.or.ke',
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'user_type': 'nurse',
                    'phone_number': '+254-700-000001',
                    'license_number': 'NUR001',
                    'specialization': 'Critical Care',
                    'years_of_experience': 5
                }
            ]

            for worker_data in workers:
                user, created = User.objects.get_or_create(
                    username=worker_data['username'],
                    defaults=worker_data
                )
                
                if created:
                    user.set_password('password123')
                    user.save()
                    
                    # Create health worker profile
                    profile, profile_created = HealthWorkerProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'license_number': worker_data['license_number'],
                            'specialization': worker_data['specialization'],
                            'years_of_experience': worker_data['years_of_experience'],
                            'primary_facility': facility,
                            'is_licensed': True
                        }
                    )
                    
                    if profile_created:
                        self.stdout.write(f'✅ Sample health worker created: {user.get_full_name()}')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Sample health workers creation failed: {e}')
            )

    def create_sample_patients(self):
        """Create sample patients."""
        try:
            facility = HealthFacility.objects.get(name='Kenyatta National Hospital')
            location = Location.objects.get(name='Nairobi County')
            
            patients = [
                {
                    'patient_id': 'P001',
                    'first_name': 'Mary',
                    'last_name': 'Wanjiku',
                    'date_of_birth': date(1985, 6, 15),
                    'gender': 'F',
                    'phone_number': '+254-700-000100',
                    'address': '123 Kimathi Street, Nairobi',
                    'location': location,
                    'registered_facility': facility,
                    'emergency_contact_name': 'John Wanjiku',
                    'emergency_contact_phone': '+254-700-000101',
                    'emergency_contact_relationship': 'Husband',
                    'blood_type': 'O+',
                    'allergies': ['Penicillin'],
                    'chronic_conditions': ['Hypertension']
                },
                {
                    'patient_id': 'P002',
                    'first_name': 'James',
                    'last_name': 'Kamau',
                    'date_of_birth': date(1990, 3, 22),
                    'gender': 'M',
                    'phone_number': '+254-700-000200',
                    'address': '456 Moi Avenue, Nairobi',
                    'location': location,
                    'registered_facility': facility,
                    'emergency_contact_name': 'Grace Kamau',
                    'emergency_contact_phone': '+254-700-000201',
                    'emergency_contact_relationship': 'Wife',
                    'blood_type': 'A+',
                    'allergies': [],
                    'chronic_conditions': []
                }
            ]

            for patient_data in patients:
                patient, created = Patient.objects.get_or_create(
                    patient_id=patient_data['patient_id'],
                    defaults=patient_data
                )
                if created:
                    self.stdout.write(f'✅ Sample patient created: {patient.get_full_name()}')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Sample patients creation failed: {e}')
            )

    def create_sample_health_records(self):
        """Create sample health records."""
        try:
            patient = Patient.objects.get(patient_id='P001')
            facility = HealthFacility.objects.get(name='Kenyatta National Hospital')
            provider = User.objects.get(username='dr.doe')
            
            record, created = HealthRecord.objects.get_or_create(
                patient=patient,
                facility=facility,
                record_type='medical',
                defaults={
                    'record_date': datetime.now(),
                    'attending_provider': provider,
                    'chief_complaint': 'Headache and fever for 3 days',
                    'history_of_present_illness': 'Patient reports severe headache and fever starting 3 days ago',
                    'assessment': 'Suspected viral infection',
                    'treatment_plan': 'Rest, fluids, and pain management',
                    'notes': 'Follow up in 1 week if symptoms persist'
                }
            )
            
            if created:
                self.stdout.write(f'✅ Sample health record created for {patient.get_full_name()}')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Sample health records creation failed: {e}')
            )

    def create_sample_analytics(self):
        """Create sample analytics data."""
        try:
            location = Location.objects.get(name='Nairobi County')
            facility = HealthFacility.objects.get(name='Kenyatta National Hospital')
            
            metrics = [
                {
                    'metric_type': 'patient_count',
                    'value': 150,
                    'unit': 'patients',
                    'location': location,
                    'facility': facility,
                    'date': date.today(),
                    'period': 'daily'
                },
                {
                    'metric_type': 'visit_count',
                    'value': 45,
                    'unit': 'visits',
                    'location': location,
                    'facility': facility,
                    'date': date.today(),
                    'period': 'daily'
                }
            ]

            for metric_data in metrics:
                metric, created = HealthMetrics.objects.get_or_create(
                    metric_type=metric_data['metric_type'],
                    location=metric_data['location'],
                    facility=metric_data['facility'],
                    date=metric_data['date'],
                    period=metric_data['period'],
                    defaults=metric_data
                )
                
                if created:
                    self.stdout.write(f'✅ Sample metric created: {metric.get_metric_type_display()}')

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Sample analytics creation failed: {e}')
            )
