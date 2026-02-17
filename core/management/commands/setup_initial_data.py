# core/management/commands/setup_initial_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import StaffProfile
from visas.models import VisaCategory

class Command(BaseCommand):
    help = 'Sets up initial data for the visa consultancy system'
    
    def handle(self, *args, **kwargs):
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@visaconsultancy.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        # Create sample staff
        if not User.objects.filter(username='staff1').exists():
            staff_user = User.objects.create_user(
                username='staff1',
                email='staff@visaconsultancy.com',
                password='staff123',
                first_name='John',
                last_name='Doe',
                is_staff=True
            )
            StaffProfile.objects.create(
                user=staff_user,
                phone='+1234567890',
                department='Visa Processing',
                designation='Senior Consultant',
                is_agent=True
            )
            self.stdout.write(self.style.SUCCESS('Staff user created'))
        
        # Create sample visa categories
        visa_categories = [
            {
                'name': 'Student Visa - USA',
                'slug': 'student-visa-usa',
                'category_type': 'STUDY',
                'description': 'For students pursuing education in the United States',
                'requirements': 'Acceptance letter, Financial proof, English proficiency',
                'processing_time': '4-8 weeks',
                'validity_period': 'Duration of study + 60 days',
                'fee': 500.00,
            },
            {
                'name': 'Work Visa - Canada',
                'slug': 'work-visa-canada',
                'category_type': 'WORK',
                'description': 'For skilled workers immigrating to Canada',
                'requirements': 'Job offer, LMIA, Work experience, Language test',
                'processing_time': '6-12 weeks',
                'validity_period': '1-3 years',
                'fee': 750.00,
            },
            {
                'name': 'Tourist Visa - Europe',
                'slug': 'tourist-visa-europe',
                'category_type': 'TOURIST',
                'description': 'Schengen tourist visa for European travel',
                'requirements': 'Travel itinerary, Hotel booking, Travel insurance',
                'processing_time': '2-4 weeks',
                'validity_period': '90 days',
                'fee': 300.00,
            },
        ]
        
        for visa_data in visa_categories:
            if not VisaCategory.objects.filter(slug=visa_data['slug']).exists():
                VisaCategory.objects.create(**visa_data)
        
        self.stdout.write(self.style.SUCCESS('Visa categories created'))
        self.stdout.write(self.style.SUCCESS('Initial setup complete!'))