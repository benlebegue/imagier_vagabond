from django.shortcuts import render, get_object_or_404

from ..expos.models import Illustrateur, Theme, Exposition
from .models import Rubrique, Page, Bloc


def homepage(request):
    """
    Render the site's home page
    """

    presentation = Bloc.objects.get(url="accueil-presentation", public=True)
    illus = Illustrateur.objects.filter(public=True).order_by("?")[0:16]
    themes = Theme.objects.order_by("?")[0:28]
    some_expos = Exposition.objects.filter(public=True, selection=True).order_by("?")[0:4]

    return render(
        request,
        "pages/homepage.html",
        {
            "nav_keyword": "home",
            "presentation": presentation,
            "some_illus": illus,
            "some_themes": themes,
            "some_expos": some_expos,
        },
    )


def catindex(request, category_url):
    """
    Render an index page that list articles in a given category
    """

    cat = get_object_or_404(Rubrique, url=category_url)
    pages = Page.objects.filter(public=True, rubrique=cat.pk)

    return render(
        request,
        "pages/catindex.html",
        {
            "nav_keyword": cat.url,
            "this_category": cat,
            "this_cat_pages": pages,
        },
    )


def page(request, category_url, article_url):
    """
    Render a single content page
    """

    page = get_object_or_404(Page, url=article_url, public=True)
    cat_pages = Page.objects.filter(public=True, rubrique__url=category_url)
    illus = (
        Illustrateur.objects.filter(public=True)
        if category_url == "liens" and article_url == "illustrateurs"
        else None
    )

    return render(
        request,
        "pages/page.html",
        {
            "nav_keyword": page.rubrique.url,
            "this_page": page,
            "this_cat_pages": cat_pages,
            "all_illus": illus,
        },
    )
