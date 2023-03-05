from django.contrib.auth.models import User as DjangoUserModel
from django.db import models


class PlansEnum(models.TextChoices):
    BASIC = "Basic"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"

class Plan(models.Model):
    plan = models.CharField(max_length=64)
    thumbnail_sizes = models.ManyToManyField("ThumbnailSize", through="PlanThumbnailSize")
    generate_binary_image = models.BooleanField(default=False)

    def __str__(self):
        return self.plan


class UserProfile(models.Model):
    user = models.OneToOneField(DjangoUserModel, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"User {self.user} with {self.plan} plan"

class ThumbnailSize(models.Model):
    name = models.CharField(max_length=128)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    plans = models.ManyToManyField(Plan, through="PlanThumbnailSize")

    def __str__(self):
        return self.name

class PlanThumbnailSize(models.Model):
    plan = models.ForeignKey(Plan, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(ThumbnailSize, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.plan} - {self.size.name}'

def get_upload_path(instance, filename):
    return f'uploads/{instance.user.username}/{filename}'

class File(models.Model):
    user = models.ForeignKey(DjangoUserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to=get_upload_path)
    binary_image = models.TextField(blank=True, null=True)
    binary_image_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.file.name
    
    @property
    def urls(self):
        results = {}
        for link in self.links.all():
            results[link.thumbnail_type.name] = link.link
        return results

class FileLink(models.Model):
    file = models.ForeignKey(File, related_name="links", on_delete=models.CASCADE)
    thumbnail_type = models.ForeignKey(ThumbnailSize, on_delete=models.CASCADE)
    link = models.TextField(default="pustylink")

    def __str__(self):
        return f"File {self.file}"