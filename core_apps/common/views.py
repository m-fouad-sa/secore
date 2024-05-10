from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
class ProjectList(ListCreateAPIView):
    #queryset = Project.objects.select_related("applicant").all()
    serializer_class = ProjectSerializer
    def get_queryset(self, *args, **kwargs):
        return Project.objects.select_related("applicant").all()

class ProjectDetail(RetrieveUpdateDestroyAPIView):
    lookup_field='id'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer 
      
class StatusList(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSertializer

class StatusDetail(RetrieveUpdateDestroyAPIView):
    lookup_field='id'
    queryset = Status.objects.all()
    serializer_class = StatusSertializer


class SectorList(ListCreateAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class SectorDetail(RetrieveUpdateDestroyAPIView):
    lookup_field='id'
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class AttachmentList(ListCreateAPIView):
    lookup_field = 'id'
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def post(self, request, *args, **kwargs):
        attachments = request.FILES.getlist('attachments')
        total_size = 0
        
        for attachment in attachments:
            total_size += attachment.size  # Add the size of each attachment
        
        # Convert total size to a more readable format (e.g., MB)
        total_size_mb = total_size / (1024 * 1024)  # Convert bytes to MB

        # If you need to restrict the size, you can check it here
        max_allowed_size = getattr(settings, "MAX_ATTACHMENT_SIZE", None)
        if max_allowed_size and total_size > max_allowed_size:
            return Response({"error": "Total attachment size exceeds the maximum allowed size."}, status=400)

        return super().post(request, *args, **kwargs)

class AttachmentDetail(RetrieveUpdateDestroyAPIView):
    lookup_field='id'
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    
