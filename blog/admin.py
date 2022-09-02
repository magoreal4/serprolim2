from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from .models import BlogPage

class BlogPageAdmin(ThumbnailMixin, ModelAdmin):
    model = BlogPage
    menu_label = "Publicaciones"
    menu_icon = "clipboard-list"
    list_display = ('admin_thumb', 'title', 'order', 'last_published_at')
    # list_editable = ('title')
    list_display_add_buttons = ('title') 

    thumb_image_field_name = 'image'

modeladmin_register(BlogPageAdmin)