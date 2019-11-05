import django_filters

from images.models import Creator, Image


class CreatorFilter(django_filters.FilterSet):
    class Meta:
        model = Creator
        fields = [
            "id",
            "name",
            "post_count",
            "followers_count",
            "following_count",
            "username",
        ]


class ImageFilter(django_filters.FilterSet):
    class Meta:
        model = Image
        fields = ["id", "caption", "like_count", "tags"]
