from django import forms
from .models import ContactInquiry, GetInvolvedInquiry, ConsultationBooking, NewsletterSubscription

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'subject', 'department', 'message', 'agree_privacy']

class GetInvolvedForm(forms.ModelForm):
    class Meta:
        model = GetInvolvedInquiry
        fields = ['name', 'email', 'organization', 'how_involved', 'message']

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationBooking
        fields = ['name', 'phone', 'service', 'preferred_date', 'additional_info']

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']