from django.db import models


def imgpath_visuel(obj, original_filename):
    """
    Function defining where to store files for the Article model,
    relative to MEDIA_ROOT, and how to name those files.
    This should provide paths such as MEDIA_ROOT/agenda/slug.jpg.
    """
    extension = original_filename.rsplit(".", 1)[1].lower()
    if obj.url:
        return "agenda/%s.%s" % (obj.url, extension)
    else:
        return "agenda/unknown/%s" % original_filename


class Article(models.Model):
    """
    Simple blog-like articles. This is so the owner of the Imagier Vagabond
    can publish news from time to time.
    No comments feature is envisionned.
    """

    titre = models.CharField("titre de larticle", max_length=100)
    url = models.SlugField("URL", max_length=100, unique=True)
    public = models.BooleanField("article public", default=False)
    pubdate = models.DateTimeField("date de publication", blank=False)
    visuel = models.ImageField("visuel", upload_to=imgpath_visuel, blank=True)
    chapo = models.TextField("texte introductif", blank=True)
    texte = models.TextField("contenu principal de l’article", blank=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "article de l’agenda"
        verbose_name_plural = "articles de l’agenda"
        ordering = ["-pubdate"]


class Programme(models.Model):
    """
    An event entry related to the expos.Exposition model. Expositions can
    be shown in different events, and we want to publish information on these
    events, anounce them beforehand, etc.
    """

    evenement = models.CharField("nom de l’évènement", max_length=100)
    lieu = models.CharField("lieu de l’animation", max_length=60)
    url = models.SlugField("URL", max_length=160, unique=True)
    public = models.BooleanField("programmation publique", default=False)
    date1 = models.DateField("date de début", blank=True)
    date2 = models.DateField("date de fin", blank=True)
    expositions = models.ManyToManyField(
        "expos.Exposition", verbose_name="expositions présentées", blank=True
    )
    lieninfo = models.URLField("informations supplémentaires (lien)", blank=True)
    texteinfo = models.TextField("texte d’information (facultatif)", blank=True)

    def __str__(self):
        return "%s à %s" % (self.evenement, self.lieu)

    class Meta:
        verbose_name = "évènement programmé (vagabondage)"
        verbose_name_plural = "évènements programmés (vagabondages)"
        ordering = ["-date1"]
