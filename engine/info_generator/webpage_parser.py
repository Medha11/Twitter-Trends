'''

    Create an awesome generalized content extractor.
    Will need appropriate research.
    Also if content is ambiguous, return nothing.
    Again storage of results have to appropriately selected like MySQL, Mongo, etc.

    The content should be limited in size, so will require proper cropping.
    Ensure sentence is not cropped midway.

'''
from goose import Goose
from utilities.mongo import get_urls
from details.models import Topic

URLs = get_urls()
for url in URLs:
    g = Goose({'browser_user_agent': 'Mozilla'})
    article = g.extract(url=url)
    if len(article.cleaned_text[:500]) > 300:
        print article.title
        print article.cleaned_text[:500]
        Topic(article_head=article.title)
        Topic(article_body=article.cleaned_text[:500])