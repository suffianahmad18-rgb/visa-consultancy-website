# testimonials/views.py
from django.views.generic import ListView
from .models import Testimonial

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'
    
    def get_queryset(self):
        return Testimonial.objects.filter(is_approved=True).order_by('-is_featured', '-created_at')

class StudyVisaTestimonialsView(ListView):
    model = Testimonial
    template_name = 'testimonials/study_visa_testimonials.html'
    context_object_name = 'testimonials'
    
    def get_queryset(self):
        return Testimonial.objects.filter(
            is_approved=True,
            visa_category='STUDY_VISA'
        ).order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add stats for study visas
        context['total_study_testimonials'] = self.get_queryset().count()
        context['top_countries'] = ['USA', 'UK', 'Canada', 'Australia', 'Germany']
        return context