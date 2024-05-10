import uuid
from django.db import models
from django.contrib.auth import get_user_model
from core_apps.profiles.models import Profile,Company
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.
# User = get_user_model()
ex_validator = FileExtensionValidator(["pdf", "doc","docx"])
# Create your models here.


class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class Project(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name=_("Profile"),
    )

    sector = models.OneToOneField(
        "Sector", on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.OneToOneField(
        "Status", on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField()
    domain = models.OneToOneField(
        "Domain", on_delete=models.CASCADE, blank=True, null=True
    )
    client = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("Company"),
    )
    attachment = models.ForeignKey(
        "Attachment", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class System(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    system_information = models.TextField()
    security_concern = models.TextField()
    status = models.OneToOneField("Status", on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


"""
class SystemSecurityStandard(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    #security_standard = models.ForeignKey(Security_Standard, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('system', 'security_standard')

    def __str__(self):
        return f"{self.system.name} - {self.security_standard.name}"

"""


class Security_Requirement(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    weight = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Security_Vulnerability(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    likelihood = models.IntegerField()
    impact = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Control_Question(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    control_question = models.TextField()
    line_number = models.PositiveIntegerField()

    class Meta:
        ordering = ["line_number"]

    def __str__(self):
        return f"Line {self.line_number}: {self.text}"


class Test_Case(TimeStampedUUIDModel):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    question = models.ForeignKey("Control_Question", on_delete=models.CASCADE)
    tag = models.CharField(max_length=25)
    description = models.TextField()
    recommendation = models.TextField()
    note = models.TextField()
    attachment = models.ForeignKey("Attachment", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Attachment(TimeStampedUUIDModel):
    name = models.CharField(max_length=64)
    attachment = models.FileField(upload_to="attachment/", validators=[ex_validator])
    description = models.CharField(max_length=50, blank=True, null=True)
    size = models.FloatField(null=True) # Size in bytes
    
    def save(self, *args, **kwargs):
        if not self.size and self.attachment:
            # Calculate and assign the size of the file
            self.size = self.attachment.size  # Assuming 'file' is a FileField
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Status(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    STATUS_CHOICES = (
        ("ongoing", "Ongoing"),
        ("ongoing evaluation", "Ongoing Evaluation"),
        ("completed", "Completed"),
        ("archived", "Archived"),
        ("active", "Active"),
        ("scheme in progress", "Scheme In Progress"),
        ("completed scheme", "Completed Scheme"),
        ("completed scheme & test plan", "Completed Scheme & Test Plan"),
        ("full", "Full"),
        ("partial", "Partial"),
        ("falied", "Falied"),
        ("passed", "Passed"),
        ("pending", "Pending"),
    )
    name = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class Sector(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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
    name = models.CharField(max_length=50, choices=SECTOR_CHOICES)

    def __str__(self):
        return self.name


class Domain(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
