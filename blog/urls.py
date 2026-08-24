from django.urls import path
from blog.views import index, postdetailview


app_name = "blog"
urlpatterns = [
    path("", index, name="index"),
    path("posts/<int:pk>/", postdetailview, name="post-detail")
]
