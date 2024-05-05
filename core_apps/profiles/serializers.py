from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
User =get_user_model

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username",read_only=True)
    email = serializers.EmailField(source="user.email",read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "profile_photo",
            "phone_number",
            "about_me",
            "gender",
            "country",
            "city",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url
    
    

    
class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            ]
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_instance = instance.user

        # Update first_name and last_name in the User model
        user_instance.first_name = user_data.get('first_name', user_instance.first_name)
        user_instance.last_name = user_data.get('last_name', user_instance.last_name)
        user_instance.save()

        # Update other fields in UserProfile model if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance        