from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.images.models import Image

from wagtail.admin.edit_handlers import (
    FieldPanel,
    # FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    # PageChooserPanel,
    # StreamFieldPanel,
)

from base.fields import MonospaceField

class HomePage(Page):
# BANNER
    subtitle = models.CharField(
        "Sub Titulo",
        max_length=50,
        blank=True,
        null=True,
        help_text="Subitulo",
        )
    slogan = models.TextField(
        "Slogan",
        blank=True,
        null=True,
        help_text="Slogan",
        )
    imageBG = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    imageMain = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    imagePromo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
# COTIZA
    cotizaDescription = models.CharField(
        "Descripcion",
        max_length=350,
        blank=True,
        null=True,
        help_text="Descripcion Cotizar",
        )
    mjeCotiza = models.CharField(
        "Cotiza",
        max_length=200,
        blank=True,
        null=True,
        help_text="Mensaje de Cotiza una que se selecciona el lugar",
        )
    mjeFueraDeRango = models.CharField(
        "Fuera de Rango",
        max_length=200,
        blank=True,
        null=True,
        help_text="La posición esta fuera del rango que se tiene en los mapas",
        )
    mjeWAContratando = models.CharField(
        "Whatsapp Contratando",
        max_length=200,
        blank=True,
        null=True,
        help_text="Mensaje Whatsapp Contratando servicio",
        )
    mjeWAFueraDeRango = models.CharField(
        "Whatsapp Fuera de rango",
        max_length=200,
        blank=True,
        null=True,
        help_text="Mensaje Whatsapp fuera de rango",
        )
# NUESTROS SERVICIOS
    serviviosDescription = models.CharField(
        "Servicios",
        max_length=350,
        blank=True,
        null=True,
        help_text="Nuestros Servicios",
        )
    
    displayNServicios = models.BooleanField(
        "Mostrar",
        default=True,
        help_text="Mostrar Cards de Nuestros Segicios",
        )


    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("slogan"),
        FieldPanel("imageBG"),
        FieldPanel("imageMain"),
        FieldPanel("imagePromo"),

        MultiFieldPanel([
            FieldPanel("cotizaDescription", classname="full"),
            FieldPanel("mjeCotiza", classname="full"),
            FieldPanel("mjeFueraDeRango", classname="full"),
            FieldPanel("mjeWAContratando", classname="full"),
            FieldPanel("mjeWAFueraDeRango", classname="full"),
        ], heading="Cotiza"),

        MultiFieldPanel([
            FieldPanel("serviviosDescription", classname="full"),
            FieldPanel("displayNServicios"),
            InlinePanel("nuestros_servicios", label="Nuestros Servicios"),
        ], heading="Nuestros Servicios"),
        
        InlinePanel("preguntas_frecuentes", label="Preguntas Frecuentes"),
    ]

class nuestrosServicios(Orderable):
    page = ParentalKey(
        HomePage, 
        on_delete=models.CASCADE, 
        related_name='nuestros_servicios'
        )
    image = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.CASCADE,
        blank = True,
        null= True,
        related_name='+'
        )
    titulo = models.CharField(
        blank=False,
        max_length=25
        )
    resumen = models.CharField(
        blank=True,
        null=True,
        max_length=250
        )

    panels = [
        FieldPanel('image'),
        FieldPanel('titulo'),
        FieldPanel('resumen'),
    ]

class preguntasFrecuentes(Orderable):
    page = ParentalKey(
        HomePage, 
        on_delete=models.CASCADE, 
        related_name='preguntas_frecuentes'
        )
# PREGUNTAS FRECUENTES
    pregunta = models.CharField(
        "Pregunta",
        max_length=250,
        blank=True,
        null=True,
        )
    respuesta = MonospaceField(
        "Respuesta",
        max_length=500,
        blank=True,
        null=True,
        )
    display = models.BooleanField(
        "Mostrar",
        default=True,
        help_text="Mostrar Pregunta y Respuesta",
        )
    panels = [
        FieldPanel('pregunta'),
        FieldPanel('respuesta'),
        FieldPanel('display'),
    ]
    # effects_image = models.BooleanField(
    #     "Efectos Imagenes", 
    #     default=True, 
    #     help_text="Efecto imagen Aro"
    #     )
    # repeat = models.BooleanField(
    #     "Repetición", 
    #     default=False, 
    #     help_text="Repite indefinidamente"
    #     )
    # effects_text = models.BooleanField(
    #     "Efectos Texto", 
    #     default=True, 
    #     help_text="Efectos de texto"
    #     )
    # # PROMOCION
    # title_promo = models.CharField(
    #     "Titulo",
    #     max_length=20,
    #     default="Ahora",
    #     blank=True,
    #     null=True,
    #     help_text="Titulo Promocion, si queda vacio no se mostrará la Promoción"
    # )
    # precio_promo = models.IntegerField(
    #     "Precio",
    #     default="30",
    #     blank=True,
    #     null=True,
    #     help_text="Precio"
    # )

    # unidad_promo = models.CharField(
    #     "Unidad",
    #     max_length=10,
    #     default="persona",
    #     blank=True,
    #     null=True,
    #     help_text="Unidad (persona/grupo/equipo"
    # )
    # descripcion_promo = models.TextField(
    #     "Descripción",
    #     max_length=50,
    #     default="",
    #     blank=True,
    #     null=True,
    #     help_text="Descripcion Corta"
    # )
     
    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request)
    #     context['servicios'] = ServicesPage.objects.first()
    #     return context

    # # mixturecards = StreamField(
    # #     [
    # #         ("mixturecards", ImageCaptionBlock()),
    # #     ],
    # #     null=True,
    # #     blank=True
    # # )
        
    # content_panels = Page.content_panels + [
    #     FieldPanel("subtitle"),
    #     FieldPanel('description'),

    #     MultiFieldPanel([
    #         FieldPanel("title_promo"),
    #         FieldPanel("precio_promo"),
    #         FieldPanel("unidad_promo"),
    #         FieldPanel("descripcion_promo"),
    #         InlinePanel("promo_features", label="Caracteristicas"),
    #     ], heading="Promoción"),

    #     MultiFieldPanel([
    #         FieldPanel("slideTime"),
    #         FieldPanel("effects_image"),
    #         FieldPanel("effects_text"),
    #         FieldPanel("repeat"),
    #         InlinePanel("carousel_images", max_num=5, min_num=1, label="Imagenes Carrosel"),
    #     ], heading="Imagenes Carrusel"),

        # MultiFieldPanel([
        #     StreamFieldPanel("mixturecards"),
        # ], heading="Servicios xxx"),
    
    # ]
