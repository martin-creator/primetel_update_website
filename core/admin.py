from django.contrib import admin
from .models import News, ContactInquiry, GetInvolvedInquiry, ConsultationBooking, NewsletterSubscription

admin.site.register(News)
admin.site.register(ContactInquiry)
admin.site.register(GetInvolvedInquiry)
admin.site.register(ConsultationBooking)
admin.site.register(NewsletterSubscription)

