from multiprocessing import context
from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api.settings.local import DEFAULT_FROM_EMAIL

from .exceptions import NotYourProfile
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)