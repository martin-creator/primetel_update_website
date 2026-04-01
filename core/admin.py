from django.contrib import admin
from .models import News, ContactInquiry, GetInvolvedInquiry, ConsultationBooking, NewsletterSubscription, AnnualReport, GalleryItem, SiteSettings

admin.site.register(News)
admin.site.register(ContactInquiry)
admin.site.register(GetInvolvedInquiry)
admin.site.register(ConsultationBooking)
admin.site.register(NewsletterSubscription)
admin.site.register(AnnualReport)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'order', 'created_at']
    list_editable = ['order']
    list_filter = ['media_type', 'category']

