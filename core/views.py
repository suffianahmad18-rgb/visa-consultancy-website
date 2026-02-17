# core/views.py - Update with contact view
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import ContactForm
from study_destinations.models import StudyDestination

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_destinations'] = StudyDestination.objects.filter(
            is_published=True, 
            is_featured=True
        ).order_by('order')[:6]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class FAQView(TemplateView):
    template_name = 'core/faq.html'

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            # In production, you would:
            # 1. Save to database
            # 2. Send email notification
            # 3. Send confirmation email to user
            
            messages.success(request, 'Thank you for your message! We will contact you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})