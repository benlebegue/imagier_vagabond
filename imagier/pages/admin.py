from django.contrib.admin import ModelAdmin, register

from .models import Rubrique, Bloc, Page


@register(Rubrique)
class RubriqueAdmin(ModelAdmin):
    list_display = (
        "nom",
        "url",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nom",
                    "url",
                ),
            },
        ),
    )
    prepopulated_fields = {
        "url": ("nom",),
    }


@register(Page)
class PageAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "titre",
                    "url",
                    "public",
                    "rubrique",
                ),
            },
        ),
        (
            "Contenus de la page",
            {
                "fields": (
                    "intro",
                    "principal",
                ),
            },
        ),
    )
    prepopulated_fields = {
        "url": ("titre",),
    }
    list_display = (
        "titre",
        "rubrique",
        "public",
    )


@register(Bloc)
class BlocAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nom",
                    "url",
                    "public",
                    "rubrique",
                ),
            },
        ),
        (
            "Contenu du bloc",
            {
                "fields": ("contenu",),
            },
        ),
    )
    prepopulated_fields = {
        "url": ("nom",),
    }
    list_display = (
        "nom",
        "rubrique",
        "url",
        "public",
    )
