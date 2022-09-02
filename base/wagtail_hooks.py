

from django.templatetags.static import static

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from wagtail import hooks

from wagtailcache.cache import clear_cache

@hooks.register("register_icons")
def register_icons(icons):
    """
    Add custom SVG icons to the Wagtail admin.
    """
    # These SVG files should be in the django templates folder, and follow exact
    # specifications to work with Wagtail:
    # https://github.com/wagtail/wagtail/pull/6028
    icons.append("icons/facebook.svg")
    icons.append("icons/abstract-abstract-037.svg")
    icons.append("icons/dribbble.svg")
    icons.append("icons/cr-align-left.svg")
    icons.append("icons/cr-google.svg")
    icons.append("icons/home.svg")

    return icons

