"""tp_web_hw_instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers

import images.views as image_views

router = routers.DefaultRouter()

urlpatterns = [
    # Users
    path(r"users/explore/", image_views.CreatorViewSet.as_view({"get": "list"})),
    path(
        r"users/search/",
        image_views.CreatorSearch.as_view({"get": "list"}),
        name="search_users",
    ),
    path(
        r"users/register/",
        image_views.CreatorSearch.as_view({"post": "create"}),
        name="create_user",
    ),
    path(r"users/login/", image_views.auth_view),
    re_path(r"^users/(?P<username>[-\w]+)/$", image_views.CreatorView.as_view()),
    re_path(r"^users/follow/(?P<user_id>.+)/$", image_views.FollowView.as_view()),
    re_path(r"^users/unfollow/(?P<user_id>.+)/$", image_views.UnFollowView.as_view()),
    re_path(
        r"^users/(?P<username>[-\w]+)/followers/$", image_views.FollowersList.as_view()
    ),
    re_path(
        r"^users/(?P<username>[-\w]+)/following/$", image_views.FollowingList.as_view()
    ),
    # Comments
    re_path(
        r"^images/(?P<image_id>.+)/comments/$",
        image_views.CommentViewSet.as_view({"post": "create"}),
    ),
    re_path(
        r"^images/(?P<image_id>.+)/comments/(?P<comment_id>.+)$",
        image_views.CommentViewSet.as_view({"delete": "destroy"}),
    ),
    re_path(
        r"^images/comments/(?P<comment_id>.+)$",
        image_views.CommentViewSet.as_view({"delete": "destroy"}),
    ),
    # Likes
    re_path(
        r"^images/(?P<image_id>.+)/likes/$",
        image_views.LikeView.as_view({"post": "create", "get": "list"}),
    ),
    re_path(
        r"^images/(?P<image_id>.+)/unlikes/$",
        image_views.LikeView.as_view({"delete": "destroy"}),
    ),
    # Images
    path(
        r"images/", image_views.ImageViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        r"images/search/",
        image_views.ImageSearch.as_view({"get": "list"}),
        name="search_images",
    ),
    re_path(
        r"images/(?P<image_id>.+)/$",
        image_views.ImageSearch.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="search_images",
    ),

    re_path(r'^auth/', include('rest_framework_social_oauth2.urls')),

    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
