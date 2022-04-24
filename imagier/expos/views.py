from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

from ..pages.models import Bloc
from .models import Exposition, FicheTechnique, Galerie, Illustrateur, Theme


def list_expos(request, sort=""):
    """
    Render the list of exhibitions
    """

    order = "titre"
    if sort:
        order = "-" + order
    expos = Exposition.objects.order_by(order).filter(public=True)

    return render(
        request,
        "expos/list-expos.html",
        {
            "nav_keyword": "expos",
            "sort_expos": sort,
            "all_expos": expos,
        },
    )


def list_illus(request):
    """
    Render the list of illustrators
    """

    from random import shuffle

    all_illus = Illustrateur.objects.filter(public=True)
    all_illus_random = []
    all_illus_random.extend(all_illus)
    shuffle(all_illus_random)
    all_illus_notround = len(all_illus) % 4  # will they fit on 4 columns?

    return render(
        request,
        "expos/list-illus.html",
        {
            "nav_keyword": "illus",
            "all_illus": all_illus,
            "all_illus_random": all_illus_random,
            "all_illus_notround": all_illus_notround,
        },
    )


def fiche_illus(request, illus_url):
    """
    Render a single illustrator's page
    """

    illus = get_object_or_404(Illustrateur, url=illus_url, public=True)
    related_expos = illus.exposition_set.filter(public=True)
    all_illus = Illustrateur.objects.filter(public=True)

    return render(
        request,
        "expos/fiche-illus.html",
        {
            "nav_keyword": "illus",
            "illus": illus,
            "related": related_expos,
            "all_illus": all_illus,
        },
    )


def list_themes(request):
    """
    Render the list of themes
    """

    themes = Theme.objects.all()
    themes_info = Bloc.objects.get(url="themes-info", public=True)

    return render(
        request,
        "expos/list-themes.html",
        {
            "nav_keyword": "themes",
            "all_themes": themes,
            "themes_info": themes_info,
        },
    )


def page_theme(request, theme_url):
    """
    Render a theme's page
    """

    theme = get_object_or_404(Theme, url=theme_url)
    themes_info = Bloc.objects.get(url="themes-info", public=True)
    related_expos = Exposition.objects.filter(themes=theme.pk, public=True)

    return render(
        request,
        "expos/page-theme.html",
        {
            "nav_keyword": "themes",
            "theme": theme,
            "related": related_expos,
            "themes_info": themes_info,
        },
    )


def fiche_expo(request, expo_url):
    """
    Render an exhibition's main page
    """

    # Getting the data
    expo = get_object_or_404(Exposition, url=expo_url, public=True)
    books = expo.livres.all

    try:
        tech = FicheTechnique.objects.get(exposition=expo.pk, public=True)
    except ObjectDoesNotExist:
        tech = False

    try:
        pics = Galerie.objects.filter(exposition=expo.pk, public=True)[0].images.all()
    except:
        pics = False

    if tech:
        vat_rate = 1.055

        def to_ttc(ht):
            return round(ht * vat_rate, 2)

        def to_ht(ttc):
            return round(ttc / vat_rate, 2)

        def to_french(num):
            if isinstance(num, float):
                return ("%.2f" % num).replace(".", ",")
            else:
                return str(num)

        if tech.tarif2_1s:
            tech.tarif2 = True
            tech.tarif2_1s_ht = to_french(to_ht(tech.tarif2_1s))
            tech.tarif2_1s_ttc = to_french(tech.tarif2_1s)
            tech.tarif2_2s_ht = to_french(to_ht(tech.tarif2_2s))
            tech.tarif2_2s_ttc = to_french(tech.tarif2_2s)
            tech.tarif2_3s_ht = to_french(to_ht(tech.tarif2_3s))
            tech.tarif2_3s_ttc = to_french(tech.tarif2_3s)
            tech.tarif2_4s_ht = to_french(to_ht(tech.tarif2_4s))
            tech.tarif2_4s_ttc = to_french(tech.tarif2_4s)
            tech.tarif2_sup_ht = to_french(to_ht(tech.tarif2_sup))
            tech.tarif2_sup_ttc = to_french(tech.tarif2_sup)

        elif tech.tarif_s1 and tech.tarif_s2 and tech.tarif_s3 and tech.tarif_s4:
            tech.tarif = True
            # VAT
            tech.tarif_s1_ttc = to_ttc(tech.tarif_s1)
            tech.tarif_s2_ttc = to_ttc(tech.tarif_s2)
            tech.tarif_s3_ttc = to_ttc(tech.tarif_s3)
            tech.tarif_s4_ttc = to_ttc(tech.tarif_s4)
            # Summing it up (no VAT)
            tech.tarif_upto_s2 = tech.tarif_s1 + tech.tarif_s2
            tech.tarif_upto_s3 = tech.tarif_upto_s2 + tech.tarif_s3
            tech.tarif_upto_s4 = tech.tarif_upto_s3 + tech.tarif_s4
            # Summing it up (with VAT)
            tech.tarif_upto_s2_ttc = tech.tarif_s1_ttc + tech.tarif_s2_ttc
            tech.tarif_upto_s3_ttc = tech.tarif_upto_s2_ttc + tech.tarif_s3_ttc
            tech.tarif_upto_s4_ttc = tech.tarif_upto_s3_ttc + tech.tarif_s4_ttc

        else:
            tech.tarif = False
            tech.tarfi2 = False

    return render(
        request,
        "expos/fiche-expo.html",
        {
            "nav_keyword": "expos",
            "expo": expo,
            "pics": pics,
            "books": books,
            "tech": tech,
        },
    )
