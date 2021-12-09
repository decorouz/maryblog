from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from django.views.generic import ListView


# Create your views here.


# Create class base views
#
class PostListView(ListView):
    queryset = Post.published.all()
    template_name = "blog/post/list.html"
    paginate_by = 3
    context_object_name = "posts"

# Lets create a second view to display a single post


def post_detail(request, year, month, day, post):
    """ Handles the views of a single post"""
    post = get_object_or_404(Post,
                             slug=post, status="published",
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    return render(request, "blog/post/detail.html", {"post": post})
