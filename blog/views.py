from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count


# class PostListView(ListView):
#     queryset = Post.published.all()
#     template_name = "blog/post/list.html"
#     paginate_by = 3
#     context_object_name = "posts"


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is our of range deliver the last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"page": page,
                                                   "posts": posts,
                                                   "tag": tag})


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


def post_detail(request, year, month, day, post):
    """ Handles the views of a single post"""
    post = get_object_or_404(Post,
                             slug=post, status="published",
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # list of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        "tags")).order_by("-same_tags", "-published_date")[:4]

    return render(request, "blog/post/detail.html", {"post": post,
                                                     "comments": comments,
                                                     "new_comment": new_comment,
                                                     "comment_form": comment_form,
                                                     "similar_posts": similar_posts})
