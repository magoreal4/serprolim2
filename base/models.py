from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
    HelpPanel
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtailsvg.models import Svg
from wagtailsvg.blocks import SvgChooserBlock
from wagtailsvg.edit_handlers import SvgChooserPanel

from .blocks import BaseStreamBlock
from .fields import MonospaceField
from .utils import get_image_model_string


class MetadataMixin(object):
    """
    An object that can be shared on social media.
    """

    def get_meta_url(self):
        """The full URL to this object, including protocol and domain."""
        raise NotImplementedError()

    def get_meta_title(self):
        raise NotImplementedError()

    def get_object_title(self):
        return self.get_meta_title()

    def get_meta_description(self):
        raise NotImplementedError()

    def get_meta_image_url(self, request):
        """
        Get the image url to use for this object.
        Can be None if there is no relevant image.
        """
        return None

    def get_meta_image_dimensions(self):
        """
        Return width, height (in pixels)
        """
        return None, None

    # def get_twitter_card_type(self, request):
    #     """
    #     Get the Twitter card type for this object.
    #     See https://dev.twitter.com/cards/types.
    #     Defaults to 'summary' if the object has an image,
    #     otherwise 'summary'.
    #     """
    #     if self.get_meta_image_url(request) is not None:
    #         return 'summary_large_image'
    #     else:
    #         return 'summary'

class WagtailImageMetadataMixin(MetadataMixin):
    """
    Subclass of MetadataMixin that uses a Wagtail Image for the image-based metadata
    """
    def get_meta_image(self):
        raise NotImplementedError()

    def get_meta_image_rendition(self):
        meta_image = self.get_meta_image()
        if meta_image:
            filter = getattr(settings, "WAGTAILMETADATA_IMAGE_FILTER", "original")
            rendition = meta_image.get_rendition(filter=filter)
            return rendition
        return None

    def get_meta_image_url(self, request):
        meta_image = self.get_meta_image_rendition()
        if meta_image:
            return request.build_absolute_uri(meta_image.url)
        return None

    def get_meta_image_dimensions(self):
        meta_image = self.get_meta_image_rendition()
        if meta_image:
            return meta_image.width, meta_image.height
        return None, None

class MetadataPageMixin(WagtailImageMetadataMixin, models.Model):
    """An implementation of MetadataMixin for Wagtail pages."""
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=_('Search image')
    )

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            ImageChooserPanel('search_image'),
        ], _('Common page configuration')),
    ]

    def get_meta_url(self):
        return self.full_url

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_image(self):
        return self.search_image

    class Meta:
        abstract = True


@register_setting(icon='dribbble')
class Logo(BaseSetting):
    
    logo = models.ForeignKey(
        Svg,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Logo SVG'),
        help_text=_("Archivo SVG -- Ejemplo.... <svg class='w-8 h-8' xmlns='http://www.w3.org/2000/svg'    version='1.1' viewBox='0 0 350 350'>   <g transform='translate(-258.272 -38.53)'>  <path fill='currentColor' d='m342.425 ...' />    </g> </svg>")
    )

    favicon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='favicon',
        verbose_name=_('Favicon'),
        help_text=_("Archivo recomendado 180x180")
    )

    stamp_logo = models.ForeignKey(
        Svg,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('logo stamp SVG'),
    )

    panels = [
        MultiFieldPanel([
            SvgChooserPanel('logo'),
            ImageChooserPanel('favicon'),
            SvgChooserPanel('stamp_logo'),
        ], heading="Logos"),
    ]

@register_setting(icon='facebook')
class Social(BaseSetting):

    facebook = models.URLField(
        blank=True, null=True, help_text="facebook page")
    instagram = models.URLField(blank=True, null=True, help_text="instagram")
    tiktok = models.URLField(blank=True, null=True, help_text="tiktok")
    youtube = models.URLField(blank=True, null=True,
                              help_text="youtube channel")
    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("instagram"),
            FieldPanel("tiktok"),
            FieldPanel("youtube"),
        ], heading="Social Media Settings"),
    ]

@register_setting(icon='cog')
class GeneralSettings(BaseSetting):

    address = models.TextField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('Address'),
        help_text=_('Business address'),
    )

    lat = models.FloatField(
        blank=True,
        null=True,
        max_length=12,
        verbose_name=_('Latitude'),
    )

    lon = models.FloatField(
        blank=True,
        null=True,
        max_length=12,
        verbose_name=_('Longitude'),
    )

    tel = models.CharField(
        blank=True,
        null=True,
        max_length=12,
        verbose_name=_('Phone'),
        help_text=_('+591 3XXXXXXXX'),
    )

    cel = models.CharField(
        blank=True,
        null=True,
        max_length=12,
        verbose_name=_('cellular phone 1 '),
        help_text=_('+591 XXXXXXXX Whatsapp'),
    )

    cel2 = models.CharField(
        blank=True,
        null=True,
        max_length=12,
        verbose_name=_('cellular phone 2'),
        help_text=_('+591 XXXXXXXX'),
    )

    email = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('email address'),
        help_text=_('The default email address this site appears to send from. For example: "sender@example.com" or "Sender Name <sender@example.com>" (without quotes)'),
    )



    # search_num_results = models.PositiveIntegerField(
    #     default=10,
    #     verbose_name=_('Number of results per page'),
    # )
    # external_new_tab = models.BooleanField(
    #     default=False,
    #     verbose_name=_('Open all external links in new tab')
    # )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('address'),
                FieldPanel('tel'),
                FieldPanel('cel'),
                FieldPanel('cel2'),
                FieldPanel('email'),

            ],
            _('General Data')
        ),
        MultiFieldPanel(
            [
                FieldPanel('lat'),
                FieldPanel('lon'),
            ],
            _('Coordinates GPS')
        ),
    ]

    class Meta:
        verbose_name = _('General')

@register_setting(icon='cr-google')
class AnalyticsSettings(BaseSetting):
    """
    Tracking and Google Analytics.
    """
    class Meta:
        verbose_name = _('Tracking')

    ga_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('UA Tracking ID'),
        help_text=_('Your Google "Universal Analytics" tracking ID (begins with "UA-")'),
    )
    ga_g_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('G Tracking ID'),
        help_text=_('Your Google Analytics 4 tracking ID (begins with "G-")'),
    )
    ga_track_button_clicks = models.BooleanField(
        default=False,
        verbose_name=_('Track button clicks'),
        help_text=_('Track all button clicks using Google Analytics event tracking. Event tracking details can be specified in each button’s advanced settings options.'),  # noqa
    )
    gtm_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Google Tag Manager ID'),
        help_text=_('Begins with "GTM-"'),
    )
    head_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name=_('<head> tracking scripts'),
        help_text=_('Add tracking scripts between the <head> tags.'),
    )
    body_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name=_('<body> tracking scripts'),
        help_text=_('Add tracking scripts toward closing <body> tag.'),
    )

    panels = [
        HelpPanel(
            heading=_('Know your tracking'),
            content=_(
                '<h3><b>Which tracking IDs do I need?</b></h3>'
                '<p>Before adding tracking to your site, '
                '<a href="https://docs.coderedcorp.com/wagtail-crx/how_to/add_tracking_scripts.html" '  # noqa
                'target="_blank">read about the difference between UA, G, GTM, '
                'and other tracking IDs</a>.</p>'
            ),
        ),
        MultiFieldPanel(
            [
                FieldPanel('ga_tracking_id'),
                FieldPanel('ga_g_tracking_id'),
                FieldPanel('ga_track_button_clicks'),
            ],
            heading=_('Google Analytics'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('gtm_id'),
            ],
            heading=_('Google Tag Manager'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('head_scripts'),
                FieldPanel('body_scripts'),
            ],
            heading=_('Other Tracking Scripts')
        )
    ]


class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    body = StreamField(
        BaseStreamBlock(), 
        verbose_name="Page body", 
        blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
    ]