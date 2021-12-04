from django.shortcuts import render, get_list_or_404
from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.published_date.all()
    return render(request, "blog/post/list.html", {"posts": posts})


# Lets create a second view to display a single post

def post_details(request, year, month, day, post):
    """Display a single post"""
    context = {"post": post}
    post = get_list_or_404(Post, slug=post, status="published",
                           published_date__year=year, published_month=month, published_date_day=day)
    return render(request, "blog/post/detail.html", context)
