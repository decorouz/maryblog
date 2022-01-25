
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import EmailPostForm, CommentForm, PostForm, SearchForm

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


from .models import Post

from taggit.models import Tag
from django.db.models import Count

from .utils import post_pagination


def create_post(request):
    post_form = PostForm()

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save()
            return redirect('blog:post_list')

    context = {"post_form": post_form}
    return render(request, "blog/post/post_form.html", context)


def post_list(request, tag_slug=None):
    common_tags = Post.tags.all()

    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    posts, custom_range = post_pagination(request)

    context = {"custom_range": custom_range, "posts": posts, "tag": tag,
               "common_tags": common_tags}

    return render(
        request,
        "blog/post/list.html", context
    )


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
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']} "
            send_mail(subject, message, "agdev882@gmail.com",
                      [cd["receiver_email"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})


# Create class base views
#


def post_detail(request, year, month, day, post):
    """Handles the views of a single post"""
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        published_date__year=year,
        published_date__month=month,
        published_date__day=day,
    )

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
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    # list of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        "tags")).order_by("-same_tags", "-published_date")[:4]

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "similar_posts": similar_posts,
        },
    )


def post_search(request):

    results = []
    if request.method == "GET":
        search_query = request.GET.get("search_query")
        search_vector = SearchVector(
            "title", weight="A") + SearchVector("body", weight="B")
        searching = SearchQuery(search_query)
        if search_query != "":
            results = (
                Post.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, searching)).filter(rank__gte=0.3)
                .order_by("-rank")
            )
    else:
        return Post.published.all()

    return render(request, "blog/post/search.html", {"search_query": search_query, "results": results})


def about(request):
    author = Post.author
    return render(request, "about-me.html", {"author": author})
