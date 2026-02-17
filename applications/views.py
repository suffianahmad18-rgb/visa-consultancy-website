from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Application, Document
from .forms import ApplicationForm, DocumentUploadForm, ApplicationStatusUpdateForm
from accounts.models import StaffProfile
from study_destinations.models import StudyDestination

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/application_list.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or hasattr(user, 'staff_profile'):
            # Staff can see all applications
            return Application.objects.all().order_by('-submitted_date')
        else:
            # Clients can only see their own applications
            return Application.objects.filter(client=user).order_by('-submitted_date')

class ApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'applications/application_detail.html'
    context_object_name = 'application'
    
    def test_func(self):
        application = self.get_object()
        user = self.request.user
        return user == application.client or user.is_staff or hasattr(user, 'staff_profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_form'] = DocumentUploadForm()
        # ✅ MAKE SURE THIS LINE EXISTS
        context['documents'] = self.object.documents.all()
        return context

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'applications/application_form.html'
    success_url = reverse_lazy('dashboard:application_list')
    
    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.total_amount = 300.00  # Default fee
        messages.success(self.request, 'Application submitted successfully!')
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        
        # Pre-fill user data
        initial['full_name'] = self.request.user.get_full_name()
        initial['email'] = self.request.user.email
        
        # Pre-fill phone if exists in profile
        if hasattr(self.request.user, 'client_profile'):
            initial['phone_number'] = self.request.user.client_profile.phone
        
        # Pre-fill destination if passed in URL
        destination_slug = self.request.GET.get('destination')
        if destination_slug:
            try:
                dest = StudyDestination.objects.get(slug=destination_slug)
                initial['destination'] = dest
                initial['destination_country'] = dest.country_name
            except StudyDestination.DoesNotExist:
                pass
        
        return initial

@login_required
def upload_document(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('dashboard:application_detail', pk=pk)
        else:
            # ✅ ADD THIS ERROR HANDLING
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('dashboard:application_detail', pk=pk)
    
    return redirect('dashboard:application_detail', pk=pk)

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    form_class = ApplicationStatusUpdateForm
    template_name = 'applications/application_update.html'
    
    def test_func(self):
        return self.request.user.is_staff or hasattr(self.request.user, 'staff_profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Application updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('dashboard:application_detail', kwargs={'pk': self.object.pk})