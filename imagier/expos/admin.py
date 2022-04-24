from django.contrib.admin import ModelAdmin, TabularInline, register

from ..shared.admin import list_thumb_and_label, form_thumb
from .models import (
    Exposition,
    FicheTechnique,
    Livre,
    Theme,
    Illustrateur,
    Galerie,
    GalerieImage,
)


@register(Exposition)
class ExpositionAdmin(ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "titre",
                    "url",
                    "public",
                    "selection",
                ),
            },
        ),
        (
            "Vignette",
            {
                "classes": ["custom-image-display"],
                "fields": (
                    "_vignette",
                    "vignette",
                ),
            },
        ),
        (
            "Présentation de l’exposition",
            {
                "fields": (
                    "chapo",
                    "descriptif",
                ),
            },
        ),
        (
            "Classement de l’exposition",
            {
                "fields": (
                    "illustrateurs",
                    "livres",
                    "themes",
                ),
            },
        ),
    ]
    prepopulated_fields = {
        "url": ("titre",),
    }
    readonly_fields = ["_vignette"]
    filter_horizontal = ["illustrateurs", "livres", "themes"]
    list_display = ["_exposition", "public", "selection", "_illustrateurs"]
    list_filter = ["public", "selection"]
    search_fields = ["titre"]

    def _illustrateurs(self, obj):
        names = []
        for illustrateur in obj.illustrateurs.all():
            names += [str(illustrateur)]
        return ", ".join(names)

    def _vignette(self, obj):
        return form_thumb(obj.vignette)

    def _exposition(self, obj):
        return list_thumb_and_label(obj.vignette, obj.titre)


@register(FicheTechnique)
class FicheTechniqueAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "exposition",
                    "public",
                ),
            },
        ),
        (
            "Originaux et encadrement",
            {
                "fields": (
                    "info_nb_origin",
                    "info_nb_cadres",
                    "info_detail",
                    "metre_lineaire",
                ),
            },
        ),
        (
            "Éléments de scénographie",
            {
                "fields": (
                    "sceno_banniere",
                    "sceno_principal",
                    "sceno_autres",
                ),
            },
        ),
        (
            "Tarifs (nouveaux, TTC)",
            {
                "description": "Les tarifs doivent être des entiers, indiquées sans espaces, points, virgules ou symboles monétaires.<br />",
                "fields": (
                    "tarif2_1s",
                    "tarif2_2s",
                    "tarif2_3s",
                    "tarif2_4s",
                    "tarif2_sup",
                    "assurance",
                    "assurance_info",
                ),
            },
        ),
        (
            "Tarifs (anciens, hors-taxe)",
            {
                "description": "Les tarifs doivent être des entiers, indiquées sans espaces, points, virgules ou symboles monétaires.<br />",
                "fields": (
                    "tarif_s1",
                    "tarif_s2",
                    "tarif_s3",
                    "tarif_s4",
                ),
            },
        ),
    )
    list_display = (
        "exposition",
        "public",
        "info_nb_origin",
        "info_nb_cadres",
        "metre_lineaire",
    )
    search_fields = ["exposition__titre"]


class GalerieImageInline(TabularInline):
    model = GalerieImage
    extra = 4


@register(Galerie)
class GalerieAdmin(ModelAdmin):
    fieldsets = (
        (
            "Important",
            {
                "fields": (
                    "exposition",
                    "public",
                ),
            },
        ),
        (
            "Informations facultatives",
            {
                "classes": ["collapse"],
                "description": "Ces informations ne sont utiles que si une exposition propose plusieurs galeries. Autrement, ne pas les renseigner.",
                "fields": (
                    "titre",
                    "description",
                ),
            },
        ),
    )
    inlines = [GalerieImageInline]
    list_display = (
        "exposition",
        "titre",
        "public",
    )
    search_fields = ["exposition__titre"]


@register(Illustrateur)
class IllustrateurAdmin(ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "nom",
                    "prenom",
                    "url",
                    "public",
                ),
            },
        ),
        (
            "Portrait",
            {
                "classes": ["custom-image-display"],
                "fields": (
                    "_portrait",
                    "portrait",
                ),
            },
        ),
        (
            "Description",
            {
                "fields": (
                    "presentation",
                    "site_web",
                    "email",
                ),
            },
        ),
    ]
    prepopulated_fields = {
        "url": (
            "prenom",
            "nom",
        )
    }
    readonly_fields = ["_portrait"]
    list_display = ["_illustrateur", "public"]
    list_filter = ["public"]
    ordering = ["nom"]
    search_fields = ["nom", "prenom"]

    def _portrait(self, obj):
        return form_thumb(obj.portrait)

    def _illustrateur(self, obj):
        return list_thumb_and_label(obj.portrait, obj.__str__())


@register(Livre)
class LivreAdmin(ModelAdmin):
    list_display = ["titre", "annee", "editeur", "collection"]
    search_fields = ["titre", "annee", "editeur", "collection"]


@register(Theme)
class ThemeAdmin(ModelAdmin):
    prepopulated_fields = {"url": ("nom",)}
    search_fields = ["nom"]
    list_display = ["nom", "url"]
