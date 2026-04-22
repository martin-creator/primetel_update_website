from django.db import models
from django.utils.text import slugify


SITE_IMAGE_CHOICES = [
    ("about_story_image", "About: Story image"),
    ("about_team_emmanuel", "About: Emmanuel team image"),
    ("about_team_moshi", "About: Dr Epiphania Moshi team image"),
    ("about_team_elly", "About: Dr Gy Elly Martin team image"),
    ("about_team_kenneth", "About: Dr Keneth Masao team image"),
    ("about_team_albano", "About: Albano Sabino team image"),
    ("about_team_rumas", "About: Rumas team image"),
    ("about_team_einoth", "About: Einoth Saitoti team image"),
    ("services_primary_care", "Services: Primary healthcare image"),
    ("services_mental_health", "Services: Mental health image"),
    ("services_outreach", "Services: Community outreach image"),
    ("services_youth", "Services: Youth and school health image"),
    ("services_telehealth", "Services: Telehealth image"),
    ("impact_partner_moh", "Impact: Ministry of Health logo"),
    ("impact_partner_orkeeswa", "Impact: Orkeeswa logo"),
    ("impact_partner_pfq", "Impact: Partners for Equity logo"),
    ("get_involved_funders", "Get Involved: Funders / How You Can Help image"),
    ("get_involved_volunteers", "Get Involved: Volunteers image"),
    ("get_involved_partners", "Get Involved: Partners image"),
    ("get_involved_brand_ally", "Get Involved: Brand Ally image"),
]


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
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
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

class AnnualReport(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    description = models.TextField()
    cover_image = models.ImageField(upload_to='annual_reports/', blank=True, null=True)
    report_file = models.FileField(upload_to='annual_reports/files/')
    highlights = models.TextField(blank=True, help_text="Key highlights, one per line")
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} ({self.year})"


class SiteSettings(models.Model):
    """Singleton model — all admin-editable content across the site."""

    # --- Hero Images ---
    home_hero_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Home page hero image")
    about_hero_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="About page hero image")

    # --- Announcement Bar ---
    announcement_text = models.CharField(max_length=300, default="Primetel Health is now licensed as a medical clinic.")
    announcement_link = models.CharField(max_length=200, blank=True, default="/about/", help_text="URL for 'Learn more' link")
    announcement_visible = models.BooleanField(default=True)

    # --- Stats ---
    stat_ussd_users = models.PositiveIntegerField(default=3600, help_text="e.g. 3600")
    stat_people_reached = models.PositiveIntegerField(default=45000)
    stat_patients_treated = models.PositiveIntegerField(default=1000)
    stat_students_reached = models.PositiveIntegerField(default=15000)

    # --- Contact Info ---
    phone = models.CharField(max_length=50, default="+255 762 629 046")
    email = models.EmailField(default="primetelhealth@gmail.com")
    address = models.CharField(max_length=200, default="Monduli, Arusha, Tanzania")
    website = models.CharField(max_length=200, default="health.primetel.tech")

    # --- Social Links ---
    instagram_url = models.URLField(blank=True, default="https://www.instagram.com/primetel_health/")
    linkedin_url = models.URLField(blank=True, default="https://www.linkedin.com/company/primetel-health/")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site Settings"


class SiteImage(models.Model):
    key = models.CharField(max_length=100, unique=True, choices=SITE_IMAGE_CHOICES)
    image = models.ImageField(
        upload_to="site_images/",
        blank=True,
        null=True,
        help_text="Upload a replacement image for this part of the site.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "Site Image"
        verbose_name_plural = "Site Images"

    def __str__(self):
        return self.get_key_display()


class GalleryItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    CATEGORY_CHOICES = [
        ('community', 'Community'),
        ('clinic', 'Clinic'),
        ('events', 'Events'),
        ('team', 'Team'),
        ('outreach', 'Outreach'),
    ]

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo embed URL")
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class NewsletterSubscription(models.Model):  # For subscribe forms
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
