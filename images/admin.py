from django.contrib import admin

from .models import Comment, Creator, CreatorFollower, Image

admin.site.register(Creator)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(CreatorFollower)

