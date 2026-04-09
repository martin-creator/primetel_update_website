from django import template
from django.templatetags.static import static


register = template.Library()


@register.simple_tag(takes_context=True)
def site_image_url(context, key, fallback_path):
    site_images = context.get("site_images", {})
    return site_images.get(key) or static(fallback_path)
