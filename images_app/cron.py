from .models import FileLink
from django.utils import timezone


def housekeeping_job():
    links = FileLink.objects.all()

    for link in links:
        thumbnail_type = link.thumbnail_type.name
        expires_at = link.file.binary_image_expires_at
        if expires_at:
            if thumbnail_type == "Binary" and (expires_at < timezone.now()):
                link.file.binary_image = None
                link.file.binary_image_expires_at = None
                link.delete()
                link.file.save()