from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # ✅ ADD THIS
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User
from applications.models import Application

# Add these at the top of your file (keep existing imports)

# Regular user views (add these before your admin views)
class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/inbox.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).order_by('-created_at')

class SentView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/sent.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-created_at')

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'messaging/message_detail.html'
    
    def get_object(self):
        message = super().get_object()
        # Mark as read when viewed
        if message.receiver == self.request.user and not message.is_read:
            message.is_read = True
            message.save()
        return message

class ComposeMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messaging/compose.html'
    success_url = reverse_lazy('messaging:sent')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        
        # If receiver is not set, assign to first admin/staff
        if not form.instance.receiver:
            staff = User.objects.filter(is_staff=True).first()
            if staff:
                form.instance.receiver = staff
            else:
                messages.error(self.request, 'No staff member available')
                return redirect('messaging:compose')
        
        messages.success(self.request, 'Message sent successfully!')
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill from URL parameters
        receiver_id = self.request.GET.get('receiver')
        if receiver_id:
            try:
                receiver = User.objects.get(id=receiver_id)
                initial['receiver'] = receiver
            except User.DoesNotExist:
                pass
        
        application_id = self.request.GET.get('application')
        if application_id:
            try:
                app = Application.objects.get(id=application_id)
                initial['application'] = app
                initial['subject'] = f"Re: Application {app.application_id}"
            except Application.DoesNotExist:
                pass
        
        return initial

# Your existing admin views stay below...

# Admin inbox view
@method_decorator(staff_member_required, name='dispatch')
class AdminInboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/admin_inbox.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        # Show all messages where admin is receiver OR sender is client
        return Message.objects.filter(
            receiver__is_staff=True
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Message.objects.filter(
            receiver=self.request.user, 
            is_read=False
        ).count()
        return context

# Admin message detail with reply
@method_decorator(staff_member_required, name='dispatch')
class AdminMessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'messaging/admin_message_detail.html'
    
    def get_object(self):
        message = super().get_object()
        # Mark as read when viewed
        if not message.is_read:
            message.is_read = True
            message.save()
        return message
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add reply form
        context['reply_form'] = MessageForm(initial={
            'receiver': self.object.sender,
            'subject': f"Re: {self.object.subject}",
            'application': self.object.application
        })
        return context
    
    def post(self, request, *args, **kwargs):
        message = self.get_object()
        form = MessageForm(request.POST)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.receiver = message.sender
            reply.save()
            messages.success(request, 'Reply sent successfully!')
            return redirect('messaging:admin_message_detail', pk=message.pk)
        
        return self.get(request, *args, **kwargs)