from rest_framework import serializers
from core_apps.profiles.serializers import ProfileSerializer
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name","country"]
        
        
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ["id", "name"]


class StatusSertializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]


class DomainSertializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "name"]


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = [
            "id",
            "name",
            "attachment",
            "description",
            "size",
            "created_at",
            "updated_at",
        ]


class CategorySertializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


        
class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "applicant",
            "client",
            "description",
            "status",
            "attachment",
            "created_at",
            "updated_at",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "applicant",
            "description",
            "domain",
            "sector",
            "status",
            "created_at",
            "updated_at",
        ]

    applicant = ProfileSerializer()
    sector = SectorSerializer()
    status = StatusSertializer()
