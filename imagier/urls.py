from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from imagier.expos import views as expos_views
from imagier.pages import views as pages_views
#from imagier.agenda import views as agenda_views

admin.autodiscover()

admin.site.site_header = "Imagier Vagabond"
admin.site.site_title = "Admin Imagier Vagabond"
admin.site.index_title = "Administration du site"

urlpatterns = [
    # Admin application
    url(r"^admin/", admin.site.urls),
    # Expos application
    url(r"^expos/(?P<sort>inv)?$", expos_views.list_expos),
    url(r"^expos/(?P<expo_url>[a-zA-Z-]+)$", expos_views.fiche_expo),
    url(r"^illustrateurs/(?P<illus_url>[a-zA-Z-]+)$", expos_views.fiche_illus),
    url(r"^illustrateurs/$", expos_views.list_illus),
    url(r"^themes/(?P<theme_url>[a-zA-Z-]+)$", expos_views.page_theme),
    url(r"^themes/$", expos_views.list_themes),
    # Agenda application
    # url(r'^agenda/(?P<post_url>[a-zA-Z-]+)$', agenda_views.post),
    # url(r'^agenda/$', agenda_views.latest),
    # Pages application
    url(
        r"^(?P<category_url>[a-zA-Z-]+)/(?P<article_url>[a-zA-Z-]+)$", pages_views.page
    ),
    url(r"^(?P<category_url>[a-zA-Z-]+)/$", pages_views.catindex),
    url(r"^$", pages_views.homepage),
]

urlpatterns += staticfiles_urlpatterns()
