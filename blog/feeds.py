from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = "May's Blog"
    link = reverse_lazy("blog:post_list")
    description = "New post of mary's blog."

    def items(self):
        """Retrieves the object to be included in the feed"""
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
