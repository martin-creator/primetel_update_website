from django.contrib import admin
from .models import (
    AnnualReport,
    ConsultationBooking,
    ContactInquiry,
    GalleryItem,
    GetInvolvedInquiry,
    News,
    NewsletterSubscription,
    SiteImage,
    SiteSettings,
)

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


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ["slot_name", "key", "image_uploaded", "updated_at"]
    list_filter = ["key"]
    search_fields = ["key"]
    ordering = ["key"]

    @admin.display(description="Image Slot")
    def slot_name(self, obj):
        return obj.get_key_display()

    @admin.display(boolean=True, description="Uploaded")
    def image_uploaded(self, obj):
        return bool(obj.image)

