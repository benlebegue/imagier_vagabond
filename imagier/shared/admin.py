from urllib.parse import quote
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe


def list_thumb_and_label(image, text):
    """
    Generate HTML for an image and label, that can be injected in a Django admin table
    """
    # Use a 120x120 size because that's what we're using on the site pages
    url = (
        get_thumbnail(image, "120x120", crop="center").url
        if image
        else "data:image/svg+xml," + quote(MISSING_IMAGE_SVG)
    )
    return mark_safe(
        '<span class="custom-thumb-label"><img src="{url}" alt=""><span>{text}</span></span>'.format(
            text=text,
            url=url,
        )
    )


def form_thumb(image):
    if image:
        return mark_safe(
            '<a class="custom-form-thumb" href="{link}"><img src="{image}"></a>'.format(
                link=image.url,
                image=get_thumbnail(image, "120x120", crop="center").url,
            )
        )
    else:
        return mark_safe(
            '<span class="custom-form-thumb"><img alt="" src="{image}"></span>'.format(
                image="data:image/svg+xml," + quote(MISSING_IMAGE_SVG),
            )
        )


MISSING_IMAGE_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="#aaa">
  <path d="M0 4V0h4v1.5H1.5V4H0zm13-4H9v1.5h4V0zm5 0v1.5h4V0h-4zm9 0v1.5h4V0h-4zm9 0v1.5h2.5V4H40V0h-4zm4 9h-1.5v4H40V9zm0 9h-1.5v4H40v-4zm0 9h-1.5v4H40v-4zm0 9h-1.5v2.5H36V40h4v-4zm-9 4v-1.5h-4V40h4zm-9 0v-1.5h-4V40h4zm-9 0v-1.5H9V40h4zm-9 0v-1.5H1.5V36H0v4h4zm-4-9h1.5v-4H0v4zm0-9h1.5v-4H0v4zm0-9h1.5V9H0v4z"/>
</svg>
"""
