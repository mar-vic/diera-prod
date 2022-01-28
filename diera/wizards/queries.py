from cms.models import Page

def get_festival_choices():
    """Return the choices representing all festival pages."""
    festival_pages = Page.objects.filter(reverse_id='festivals').filter(publisher_is_draft=False).first().get_child_pages()
    # Choices are tuples made of key/value pairs
    return [(fp.id, fp.get_title()) for fp in festival_pages]
