# study_destinations/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import StudyDestination

class StudyDestinationListView(ListView):
    model = StudyDestination
    template_name = 'study_destinations/destination_list.html'
    context_object_name = 'destinations'
    
    def get_queryset(self):
        return StudyDestination.objects.filter(is_published=True).order_by('order', 'country_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_destinations'] = StudyDestination.objects.filter(
            is_published=True, 
            is_featured=True
        ).order_by('order')[:4]
        return context

class StudyDestinationDetailView(DetailView):
    model = StudyDestination
    template_name = 'study_destinations/destination_detail.html'
    context_object_name = 'destination'
    slug_field = 'slug'
    
    def get_queryset(self):
        return StudyDestination.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.object
        
        # Get all related data
        context['sections'] = destination.sections.filter(is_active=True).order_by('order')
        context['tuition_fees'] = destination.tuition_fees.all().order_by('order')
        context['intakes'] = destination.intakes.all().order_by('order')
        context['scholarships'] = destination.scholarships.filter(is_active=True).order_by('order')
        context['visa_requirements'] = destination.visa_requirements.all().order_by('order')
        context['post_study_work'] = destination.post_study_work.all().order_by('order')
        
        # Related destinations
        context['related_destinations'] = StudyDestination.objects.filter(
            is_published=True
        ).exclude(id=destination.id).order_by('order')[:3]
        
        return context