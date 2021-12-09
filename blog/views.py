from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.forms import EmailPostForm
from .models import Post
from django.views.generic import ListView


# Create your views here.
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommend you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']} "
            send_mail(subject, message, "agdev882@gmail.com",
                      [cd['receiver_email']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html",  {"post": post, "form": form, "sent": sent})

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
