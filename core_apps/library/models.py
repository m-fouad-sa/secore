from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.


class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class Security_Standard(TimeStampedUUIDModel):
    SECTOR_CHOICES = [
        ("IT", "Information Technology"),
        ("Finance", "Finance"),
        ("Healthcare", "Healthcare"),
        ("Manufacturing", "Manufacturing"),
        ("Retail", "Retail"),
        ("Real Estate", "Real Estate"),
        ("Education", "Education"),
        ("Transportation", "Transportation"),
        ("Hospitality", "Hospitality"),
        ("Energy", "Energy"),
        ("Entertainment", "Entertainment"),
        ("Agriculture", "Agriculture"),
        ("Telecommunications", "Telecommunications"),
        ("Automotive", "Automotive"),
        ("Construction", "Construction"),
        ("Media", "Media"),
        ("Pharmaceuticals", "Pharmaceuticals"),
        ("Government", "Government"),
        ("Non-Profit", "Non-Profit"),
        ("Fashion", "Fashion"),
        ("Consulting", "Consulting"),
        ("Insurance", "Insurance"),
        ("Legal", "Legal"),
        ("Advertising", "Advertising"),
        ("Banking", "Banking"),
        ("Biotechnology", "Biotechnology"),
        ("Chemical", "Chemical"),
        ("Computer", "Computer"),
        ("Defense", "Defense"),
        ("Electronics", "Electronics"),
        ("Energy", "Energy"),
        ("Food", "Food"),
        ("Healthcare", "Healthcare"),
        ("Information", "Information"),
        ("Insurance", "Insurance"),
        ("Legal", "Legal"),
        ("Manufacturing", "Manufacturing"),
        ("Media", "Media"),
        ("Mining", "Mining"),
        ("Pharmaceuticals", "Pharmaceuticals"),
        ("Real Estate", "Real Estate"),
        ("Retail", "Retail"),
        ("Software", "Software"),
        ("Technology", "Technology"),
        ("Telecommunications", "Telecommunications"),
        ("Transportation", "Transportation"),
        ("other", "other"),
    ]

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500, blank=True, null=True)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES)
