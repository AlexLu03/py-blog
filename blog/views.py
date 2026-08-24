from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Commentary
from django.core.paginator import Paginator
from blog.forms import CommentForm


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related("owner").order_by("-created_time")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "posts": posts,
        # tests expect a context variable named 'post_list'
        "post_list": page_obj,
    }

    return render(request, "blog/index.html", context=context)


def PostDetailView(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post.objects.select_related("owner"), id=pk)

    comments = Commentary.objects.filter(post=post)
    sort_param = request.GET.get("sort")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                form = CommentForm()
            else:
                form.add_error(None, "You must be logged in to post a comment.")
        else:
            if not request.user.is_authenticated:
                form.add_error(None, "You must be logged in to post a comment.")
    else:
        form = CommentForm()

    if sort_param == "time_desc":
        comments = comments.order_by("-created_time")
    elif sort_param == "time_asc":
        comments = comments.order_by("created_time")
    elif sort_param == "alpha_desc":
        comments = comments.order_by("-content")
    elif sort_param == "alpha_asc":
        comments = comments.order_by("content")

    context = {
        "post": post,
        "comments": comments,
        "sort_param": sort_param,
        "form": form,
    }

    return render(request, "blog/post_detail.html", context=context)
