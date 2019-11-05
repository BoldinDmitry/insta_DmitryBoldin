from functools import partial

from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CreatorFilter, ImageFilter
from .models import Comment, Creator, Image, Like
from .permissions import CanEditOnlyItself
from .serializers import CommentSerializer, CreatorSerializer, ImageSerializer, LikeSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class CreatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)


class CreateNewUser(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)


class CreatorSearch(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    filter_class = CreatorFilter
    authentication_classes = (CsrfExemptSessionAuthentication,)


class CreatorView(APIView):
    serializer_class = CreatorSerializer
    queryset = Creator.objects.all()
    lookup_url_kwarg = "username"
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (partial(CanEditOnlyItself, ["PUT"]),)

    def get_object(self, username):
        try:
            return self.queryset.get(username=username)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")

        creator = self.get_object(username)

        creator_serialized = CreatorSerializer(creator).data
        return Response(creator_serialized)

    def put(self, request, *args, **kwargs):
        username = kwargs.get("username")
        creator = self.get_object(username)

        serializer = self.serializer_class(creator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowView(APIView):
    object_manager = Creator.objects
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, o_id):
        try:
            return self.object_manager.get(id=o_id)
        except (ObjectDoesNotExist, ValueError):
            raise Http404

    def post(self, request, *args, **kwargs):
        """
        Follow some user
        """
        o_id = kwargs.get("user_id")
        creator = self.get_object(o_id)
        creator.follow(request.user)
        return Response({"status": "ok"})


class UnFollowView(APIView):
    object_manager = Creator.objects
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, o_id):
        try:
            return self.object_manager.get(id=o_id)
        except ObjectDoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        """
        Unfollow some user
        """
        o_id = kwargs.get("user_id")
        creator = self.get_object(o_id)
        creator.unfollow(request.user)
        return Response({"status": "ok"})


class FollowersList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = CreatorSerializer
    queryset = Creator.objects.all()

    def get_object(self, username):
        try:
            return self.queryset.get(username=username)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        """
        Get all user followers
        """
        username = kwargs.get("username")
        creator = self.get_object(username)
        followers = creator.get_followers()
        return Response(self.serializer_class(followers, many=True).data)


class FollowingList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = CreatorSerializer
    queryset = Creator.objects.all()

    def get_object(self, username):
        try:
            return self.queryset.get(username=username)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        """
        Get all user followers
        """
        username = kwargs.get("username")
        follower = self.get_object(username)
        followers = follower.get_following()
        return Response(self.serializer_class(followers, many=True).data)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.get_following_images()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_object(self):
        comment_id = self.kwargs.get("comment_id")
        try:
            return self.queryset.get(id=comment_id)
        except ObjectDoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        image_id = kwargs.get("image_id")
        data["image_id"] = image_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ImageSearch(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_class = ImageFilter
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_object(self):
        image_id = self.kwargs.get("image_id")
        try:
            return self.queryset.get(id=image_id)
        except ObjectDoesNotExist:
            raise Http404


class LikeView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_object(self):
        like_id = self.kwargs.get("image_id")
        try:
            return self.queryset.get(image__pk=like_id, person=self.request.user)
        except ObjectDoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        image_id = kwargs.get("image_id")
        data = {"image": image_id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@csrf_exempt
def auth_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("{'status': 'ok'}")
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")
