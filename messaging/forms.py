# messaging/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter receivers based on user role
            if user.is_staff:
                self.fields['receiver'].queryset = User.objects.filter(is_staff=False)
            else:
                self.fields['receiver'].queryset = User.objects.filter(is_staff=True)