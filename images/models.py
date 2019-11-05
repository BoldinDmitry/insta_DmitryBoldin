from django.contrib.auth import models as user_models
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .managers import UserManager


class Creator(user_models.AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    profile_image = models.ImageField(upload_to="profiles_images")
    name = models.CharField(max_length=255)
    bio = models.TextField()
    website = models.TextField()
    post_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    USERNAME_FIELD = "username"

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    def follow(self, follower):
        follow = CreatorFollower.objects.get_or_create(creator=self, follower=follower)
        if follow[1]:
            follower.following_count += 1
            follower.save()

            self.followers_count += 1
            self.save()

    def unfollow(self, ex_follower):
        try:
            follow = CreatorFollower.objects.get(creator=self, follower=ex_follower)
        except ObjectDoesNotExist:
            return False

        ex_follower.following_count -= 1
        ex_follower.save()

        self.followers_count -= 1
        self.save()

        follow.delete()
        return True

    def get_followers(self):
        followers_ids = CreatorFollower.objects.filter(creator=self).values_list(
            "follower", flat=True
        )
        followers = []
        for follower_id in followers_ids:
            followers.append(Creator.objects.get(pk=follower_id))

        return followers

    def get_following(self):
        creators_ids = CreatorFollower.objects.filter(follower=self).values_list(
            "creator", flat=True
        )
        creators = []
        for creator_id in creators_ids:
            creators.append(Creator.objects.get(pk=creator_id))

        return creators

    def get_following_images(self):
        all_following = self.get_following()
        all_images = []
        for following in all_following:
            all_images.extend(Image.objects.filter(creator_id=following))
        return all_images

    def __str__(self):
        return self.username


class CreatorFollower(models.Model):
    creator = models.ForeignKey(
        Creator, on_delete=models.CASCADE, related_name="creator"
    )
    follower = models.ForeignKey(
        Creator, on_delete=models.CASCADE, related_name="follower"
    )

    def __str__(self):
        return str(self.follower) + " -> " + str(self.creator)


class Image(models.Model):
    file = models.ImageField(upload_to="user_images")
    caption = models.TextField(blank=True)
    like_count = models.IntegerField(default=0)
    creator_id = models.ForeignKey(Creator, on_delete=models.CASCADE)
    tags = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator_id.post_count += 1
            self.creator_id.save()
        return super(Image, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.pk:
            self.creator_id.post_count -= 1
            self.creator_id.save()
        return super(Image, self).delete(*args, **kwargs)

    def __str__(self):
        return self.creator_id.username


class Comment(models.Model):
    message = models.TextField()
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)


class Like(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    person = models.ForeignKey(Creator, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.image.like_count += 1
            self.image.save()
        return super(Like, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.pk:
            self.image.like_count -= 1
            self.image.save()
        return super(Like, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ('image', 'person',)
