import uuid
from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

ex_validator = FileExtensionValidator(['pdf','doc'])
# Create your models here.

class Project(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)
    description = models.TextField()




class Attachment(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=64)
    attachment=models.FileField(upload_to='attachment/',validators=[ex_validator])
    description = models.TextField()


class System(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)
    system_information=models.TextField()
    security_concern=models.TextField()


class Domain(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)

class Status(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)


class Security_Requirement(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)
    control_question=models.TextField()
    weight=models.IntegerField(max_length=2)


class Security_Vulnerability(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)
    control_question=models.TextField()
    likelihood=models.IntegerField(max_length=2)
    impact=models.IntegerField(max_length=2)

class Test_Case(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)
    tag=models.CharField(max_length=255)
    description = models.TextField()
    note=models.TextField()


class Category(models.Model):
    pkid=models.BigAutoField(primary_key=True, editable=False)
    name=models.CharField(max_length=255)






class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
