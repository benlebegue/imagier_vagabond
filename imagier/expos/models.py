from urllib.parse import urlsplit
from django.db import models

from ..shared.storage import OverwriteStorage
from . import admin_help


def imgpath_vignette(obj, original_filename):
    extension = original_filename.rsplit(".", 1)[1].lower()
    if obj.url:
        return "expos/%s.%s" % (obj.url, extension)
    else:
        return "expos/unknown/%s" % original_filename


def imgpath_illus(obj, original_filename):
    extension = original_filename.rsplit(".", 1)[1].lower()
    if obj.url:
        return "illustrateur/%s.%s" % (obj.url, extension)
    else:
        return "illustrateur/unknown/%s" % original_filename


def imgpath_gallery(obj, original_filename):
    if obj.galerie_id:
        return "galeries/%s/%s" % (str(obj.galerie_id), original_filename)
    else:
        return "galeries/unknown/%s" % original_filename


class Exposition(models.Model):
    """
    Base model for the whole website. Represents a catalog of expositions, each
    with text information, links to author profiles, metadata, an image preview,
    and a link to an attached gallery.
    """

    # Base
    titre = models.CharField(
        "titre de l’exposition",
        max_length=120,
        unique=True,
    )
    url = models.SlugField(
        "URL",
        help_text=admin_help.expo_url,
        unique=True,
    )
    public = models.BooleanField(
        "publiée",
        help_text=admin_help.expo_pub,
        default=False,
    )
    selection = models.BooleanField(
        "à la une",
        help_text=admin_help.expo_selec,
        default=False,
    )

    # Metadata/links
    illustrateurs = models.ManyToManyField(
        "Illustrateur",
        blank=True,
    )
    livres = models.ManyToManyField(
        "Livre",
        blank=True,
    )
    themes = models.ManyToManyField(
        "Theme",
        blank=True,
    )

    # Content
    vignette = models.ImageField(
        blank=True,
        upload_to=imgpath_vignette,
        storage=OverwriteStorage(),
    )
    chapo = models.TextField(
        "chapeau",
        blank=True,
        help_text=admin_help.expo_chapo,
    )
    descriptif = models.TextField(
        "descriptif de l’exposition",
        blank=True,
        help_text=admin_help.expo_desc,
    )

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return "/expos/%s" % self.url

    class Meta:
        ordering = ["titre"]


class FicheTechnique(models.Model):
    """
    Model for metadata that goes along with the Exposition metadata.
    Elements of scenography or prices and technical details are listed here.
    """

    # Base
    exposition = models.OneToOneField(
        Exposition,
        verbose_name="fiche pour l’exposition…",
        on_delete=models.DO_NOTHING,
    )
    public = models.BooleanField(
        "publiée",
        help_text=admin_help.fiche_pub,
        default=False,
    )

    # Originaux et encadrement
    info_nb_origin = models.IntegerField(
        "nombre d’originaux",
        blank=False,
        help_text="Nombre de planches ou illustrations originales.",
    )
    info_nb_cadres = models.IntegerField(
        "nombre de cadres",
        blank=False,
    )
    info_detail = models.TextField(
        "détail",
        blank=True,
        help_text=admin_help.fiche_idetail,
    )
    metre_lineaire = models.IntegerField(
        "mètre linéaire",
        blank=True,
        null=True,
        help_text="Arrondir à l’unité la plus proche. Ex: <i>16</i> pour 16,3m.",
    )

    # Scénographie
    sceno_banniere = models.TextField(
        "bannière",
        blank=True,
        help_text=admin_help.fiche_sceno1,
    )
    sceno_principal = models.TextField(
        "principaux éléments",
        blank=True,
        help_text=admin_help.fiche_sceno2,
    )
    sceno_autres = models.TextField(
        "autres éléments",
        blank=True,
    )

    # Tarifs anciens
    tarif_s1 = models.IntegerField("semaine 1 (HT)", blank=True, null=True)
    tarif_s2 = models.IntegerField("semaine 2 (HT)", blank=True, null=True)
    tarif_s3 = models.IntegerField("semaine 3 (HT)", blank=True, null=True)
    tarif_s4 = models.IntegerField("semaine 4 (HT)", blank=True, null=True)

    # Assurance
    assurance = models.IntegerField(
        "valeur de l’assurance",
        blank=True,
        null=True,
    )
    assurance_info = models.CharField(
        "assurance: information complémentaire",
        blank=True,
        max_length=250,
    )

    # Tarifs nouveaux
    tarif2_1s = models.IntegerField("une semaine (TTC)", blank=True, null=True)
    tarif2_2s = models.IntegerField("deux semaines (TTC)", blank=True, null=True)
    tarif2_3s = models.IntegerField("trois semaines (TTC)", blank=True, null=True)
    tarif2_4s = models.IntegerField("quatre semaines (TTC)", blank=True, null=True)
    tarif2_sup = models.IntegerField(
        "semaine supplémentaire (TTC)", blank=True, null=True
    )

    def __str__(self):
        return "Fiche expo: %s" % self.exposition

    class Meta:
        ordering = ["exposition"]
        verbose_name = "fiche technique d’exposition"
        verbose_name_plural = "fiches techniques des expositions"


class Galerie(models.Model):
    """
    Image gallery. This model is written as an extension to the Exposition
    model.
    """

    # Base
    exposition = models.ForeignKey(
        "Exposition",
        related_name="galerie",
        verbose_name="galerie pour l’exposition…",
        on_delete=models.DO_NOTHING,
    )
    public = models.BooleanField(
        "publiée", help_text=admin_help.galerie_pub, default=False
    )

    # Options / more info
    titre = models.CharField(
        "titre de la galerie",
        max_length=100,
        blank=True,
    )
    description = models.TextField(
        "descriptif court",
        blank=True,
    )
    afficher_infos = models.BooleanField(
        "afficher sur le site",
        help_text=admin_help.galerie_infos,
        default=False,
    )

    def __str__(self):
        if self.titre:
            return "%s / %s" % (self.exposition, self.titre)
        else:
            return "%s / galerie %s" % (self.exposition, str(self.id))

    class Meta:
        verbose_name = "galerie d’images d’exposition"
        verbose_name_plural = "galeries d’images des expositions"
        ordering = ["exposition"]


class GalerieImage(models.Model):
    """
    Image item that goes into a gallery.
    """

    galerie = models.ForeignKey(
        "Galerie",
        related_name="images",
        verbose_name="image pour la galerie…",
        on_delete=models.DO_NOTHING,
    )
    image = models.ImageField(
        "fichier image",
        upload_to=imgpath_gallery,
        storage=OverwriteStorage(),
    )
    legende = models.CharField(
        "légende de l’image",
        blank=True,
        max_length=200,
    )
    position = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "image de la galerie"
        verbose_name_plural = "images de la galerie"
        ordering = ["galerie", "position", "image"]


class Illustrateur(models.Model):
    """
    A model describing an illustrator.
    """

    nom = models.CharField(
        "nom",
        help_text=admin_help.illus_nom,
        max_length=40,
    )
    prenom = models.CharField(
        "prénom",
        max_length=30,
        blank=True,
    )
    url = models.SlugField(
        "URL",
        help_text=admin_help.illus_url,
        max_length=50,
    )
    public = models.BooleanField(
        "Profil public",
        help_text=admin_help.illus_pub,
        default=False,
    )
    portrait = models.ImageField(
        "photo ou portrait",
        blank=True,
        upload_to=imgpath_illus,
        storage=OverwriteStorage(),
    )
    presentation = models.TextField(
        "texte de présentation",
        blank=True,
    )
    site_web = models.URLField(
        "site web",
        blank=True,
    )
    email = models.EmailField(
        "adresse e-mail",
        blank=True,
        help_text=admin_help.illus_eml,
    )

    def __str__(self):
        if self.prenom:
            return self.prenom + " " + self.nom
        else:
            return self.nom

    def site_web_readable(self):
        return urlsplit(self.site_web).netloc if self.site_web else False

    def email_protected(self):
        return self.email.replace("@", " (arobase) ")

    def get_absolute_url(self):
        return "/illustrateurs/%s" % self.url

    class Meta:
        ordering = ["nom", "prenom"]


class Livre(models.Model):
    """
    Simple model to store information on a book. As we don't have a complete
    database of books, authors, publishers, etc., some information is
    “hardcoded”, especially authors and publishers strings.
    """

    titre = models.CharField(
        "titre du livre",
        max_length=100,
    )
    auteurs = models.CharField(
        "auteur(s)",
        blank=True,
        max_length=200,
        help_text=admin_help.livre_aut,
    )
    editeur = models.CharField(
        "éditeur",
        max_length=50,
        blank=True,
    )
    collection = models.CharField(
        max_length=50,
        blank=True,
    )
    annee = models.CharField(
        "année de publication",
        max_length=4,
        blank=True,
    )

    def __str__(self):
        if self.editeur != "":
            return "%s (%s)" % (self.titre, self.editeur)
        else:
            return self.titre

    class Meta:
        ordering = ["titre"]


class Theme(models.Model):
    """
    Themes are topics that are shared between expositions.
    Basically these are tags.
    """

    nom = models.CharField(
        "nom du thème",
        max_length=50,
    )
    url = models.SlugField(
        "URL",
        unique=True,
        help_text=admin_help.theme_url,
    )

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return "/themes/%s" % self.url

    class Meta:
        ordering = ["url"]
        verbose_name = "thème d’exposition"
        verbose_name_plural = "thèmes des expositions"
