from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Commentary
from django.core.paginator import Paginator


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


def PostDetailView(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post.objects.select_related("owner"), id=post_id)

    comments = Commentary.objects.filter(post=post)
    sort_param = request.GET.get("sort")
    comment_error = None

    if request.method == "POST":
        content = request.POST.get("content")
        if content and request.user.is_authenticated:
            Commentary.objects.create(
                post=post,
                content=content,
                user=request.user,
            )
        else:
            comment_error = "You must be logged in to post a comment."

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
        "sort_param": sort_param,
        "comments": comments,
        "comment_error": comment_error,
    }

    return render(request, "blog/post_detail.html", context=context)
