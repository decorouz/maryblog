from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post


def post_pagination(request):

    paginator = Paginator(Post.published.all(), 5)

    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    """
    This is to ensure that we don't have insane amount of paginations
    as the post object increases with every new addition
    """

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(left_index, rightIndex)

    return posts, custom_range
