from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Comment, Creator, Image, Like


class CreatorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = super(CreatorSerializer, self).create(validated_data)
        return user

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CreatorSerializer, self).update(instance, validated_data)

    class Meta:
        model = Creator
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    creator_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Image
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(), default=serializers.CurrentUserDefault()
    )
    image = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all()
    )

    class Meta:
        model = Like
        fields = "__all__"
