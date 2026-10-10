# Clean up each page's content after the with-pdf plugin has captured it and
# before it is combined into the PDF. The HTML site is not affected.
from mkdocs.plugins import event_priority


@event_priority(-100)  # run after with-pdf's on_post_page
def on_post_page(output, page, config, **kwargs):
    article = getattr(page, 'pdf-article', None)
    if article is None:
        return output

    # glightbox wraps every image in a link to the image file. The plugin
    # leaves those relative links as-is, so they lead nowhere in the PDF and
    # its strict check reports each one as a missing link.
    for link in article.select('a.glightbox'):
        link.unwrap()

    # Code line anchors (pymdownx.highlight `anchor_linenums`) are rendered as
    # <a id="__codelineno-0-1" name="__codelineno-0-1">. The plugin rewrites
    # the id and the matching hrefs to page-scoped values but not the name,
    # and WeasyPrint prefers name over id as the anchor of an <a>, so every
    # line link fails with "No anchor ... for internal URI reference".
    for anchor in article.select('a[id][name]'):
        del anchor['name']

    return output
