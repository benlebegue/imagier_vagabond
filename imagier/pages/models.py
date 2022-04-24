from django.db import models


class Rubrique(models.Model):
    nom = models.CharField(
        "nom de la rubrique",
        max_length=100,
        unique=True,
    )
    url = models.SlugField(
        "URL",
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.nom


class Page(models.Model):
    titre = models.CharField(
        "titre de la page",
        max_length=100,
        unique=True,
    )
    url = models.SlugField(
        "URL",
        max_length=100,
        unique=True,
    )
    public = models.BooleanField(
        "page publique",
        default=False,
    )
    rubrique = models.ForeignKey(
        "Rubrique",
        on_delete=models.DO_NOTHING,
    )
    intro = models.TextField(
        "contenu d’introduction",
        blank=True,
    )
    principal = models.TextField(
        "contenu principal",
        blank=True,
    )

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return "/%s/%s" % (self.rubrique.url, self.url)

    class Meta:
        verbose_name = "page complète"
        verbose_name_plural = "pages complètes"


class Bloc(models.Model):
    nom = models.CharField(
        "nom du bloc",
        help_text="Ne sera pas affiché sur le site.",
        max_length=100,
        unique=True,
    )
    url = models.SlugField(
        "URL",
        help_text="Identifiant textuel utilisé en interne, ne sera visible sur le site.",
        max_length=100,
        unique=True,
    )
    public = models.BooleanField(
        "bloc publié",
        default=False,
    )
    rubrique = models.ForeignKey(
        "Rubrique",
        on_delete=models.DO_NOTHING,
    )
    contenu = models.TextField(
        "contenu",
        blank=True,
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "bloc de contenu"
        verbose_name_plural = "blocs de contenu"
