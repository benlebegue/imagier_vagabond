from django.contrib.admin import ModelAdmin, register

from .models import Article, Programme


@register(Article)
class ArticleAdmin(ModelAdmin):
    fields = (
        "titre",
        "url",
        "public",
        "pubdate",
        "visuel",
        "chapo",
        "texte",
    )
    prepopulated_fields = {
        "url": ("titre",),
    }


@register(Programme)
class ProgrammeAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "evenement",
                    "lieu",
                    "url",
                    "public",
                ),
            },
        ),
        (
            "Informations obligatoires",
            {
                "fields": (
                    "date1",
                    "date2",
                    "expositions",
                ),
            },
        ),
        (
            "Informations complémentaires",
            {
                "fields": (
                    "lieninfo",
                    "texteinfo",
                ),
            },
        ),
    )
    prepopulated_fields = {
        "url": (
            "evenement",
            "lieu",
        )
    }
    # filter_horizontal = ['expositions']
    list_display = (
        "evenement",
        "lieu",
        "date1",
        "date2",
        "public",
    )
    search_fields = [
        "evenement",
        "lieu",
    ]
