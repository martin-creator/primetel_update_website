from django.db import models
from django.utils.text import slugify

class News(models.Model):
    CATEGORY_CHOICES = [
        ('health_updates', 'Health Updates'),
        ('community_stories', 'Community Stories'),
        ('education', 'Education'),
        ('technology', 'Technology'),
        ('partnerships', 'Partnerships'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.CharField(max_length=200, blank=True)  # e.g., "Mental Health, Community, Training"
    author = models.CharField(max_length=100)
    date = models.DateField()
    read_time = models.IntegerField(help_text="In minutes")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    department = models.CharField(max_length=50)  # From select: General Inquiry, Partnerships, etc.
    message = models.TextField()
    agree_privacy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class GetInvolvedInquiry(models.Model):
    INVOLVE_CHOICES = [
        ('funder_donor', 'Funder/Donor'),
        ('volunteer', 'Volunteer'),
        ('organization_partner', 'Organization Partner'),
        ('fellowship_program', 'Fellowship Program'),
        ('brand_ally_csr', 'Brand Ally/CSR'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.CharField(max_length=200, blank=True)
    how_involved = models.CharField(max_length=20, choices=INVOLVE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.how_involved}"

class ConsultationBooking(models.Model):  # For book consultation forms on multiple pages
    SERVICE_CHOICES = [
        ('mental_health_counseling', 'Mental Health Counseling'),
        ('primary_care_consultation', 'Primary Care Consultation'),
        ('mobile_clinic_visit', 'Mobile Clinic Visit'),
        ('community_outreach', 'Community Outreach'),
    ]
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    preferred_date = models.DateField()
    additional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service}"

class NewsletterSubscription(models.Model):  # For subscribe forms
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email