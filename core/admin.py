from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
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

SITE_IMAGE_FALLBACKS = {
    "about_story_image": "images/primetel_story.jpg",
    "about_team_emmanuel": "images/Emmanuel_bio.jpg",
    "about_team_moshi": "images/moshi_bio.jpg",
    "about_team_elly": "images/ellymartin_bio.jpg",
    "about_team_kenneth": "images/kenneth_bio.jpg",
    "about_team_albano": "images/albano_bio.jpeg",
    "about_team_rumas": "images/rumas_bio.jpg",
    "about_team_einoth": "images/einoth_bio.jpg",
    "services_primary_care": "images/primaryhealth_care_service.jpg",
    "services_mental_health": "images/mental_health_service.jpg",
    "services_outreach": "images/outreach_services.jpg",
    "services_youth": "images/youth_mental_service.jpg",
    "services_telehealth": "images/telemedicine_service.jpg",
    "impact_partner_moh": "images/moh_logo.jpg",
    "impact_partner_orkeeswa": "images/orkeeswa_logo.jpg",
    "impact_partner_pfq": "images/pfq_logo.png",
}


def render_admin_image_preview(image_url, source_label, max_width):
    return format_html(
        (
            '<div>'
            '<img src="{}" style="max-width: {}px; height: auto; border-radius: 8px; '
            'border: 1px solid #d1d5db; background: #fff;" />'
            '<div style="margin-top: 6px; color: #6b7280; font-size: 12px;">{}</div>'
            "</div>"
        ),
        image_url,
        max_width,
        source_label,
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
    readonly_fields = ["home_hero_preview", "about_hero_preview"]

    @admin.display(description="Home hero preview")
    def home_hero_preview(self, obj):
        if obj.home_hero_image:
            return render_admin_image_preview(obj.home_hero_image.url, "Uploaded image", 320)
        return render_admin_image_preview(static("images/hero.jpg"), "Current site fallback", 320)

    @admin.display(description="About hero preview")
    def about_hero_preview(self, obj):
        if obj.about_hero_image:
            return render_admin_image_preview(obj.about_hero_image.url, "Uploaded image", 320)
        return render_admin_image_preview(
            static("images/primetel_about_header_men.jpg"),
            "Current site fallback",
            320,
        )

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'order', 'created_at']
    list_editable = ['order']
    list_filter = ['media_type', 'category']


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ["slot_name", "key", "image_preview", "image_uploaded", "updated_at"]
    list_filter = ["key"]
    search_fields = ["key"]
    ordering = ["key"]
    readonly_fields = ["image_preview"]

    @admin.display(description="Image Slot")
    def slot_name(self, obj):
        return obj.get_key_display()

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return render_admin_image_preview(obj.image.url, "Uploaded image", 160)
        fallback_path = SITE_IMAGE_FALLBACKS.get(obj.key)
        if fallback_path:
            return render_admin_image_preview(static(fallback_path), "Current site fallback", 160)
        return "No preview available."

    @admin.display(boolean=True, description="Uploaded")
    def image_uploaded(self, obj):
        return bool(obj.image)

