from django.contrib import admin
from .models import UserProfile, ThumbnailSize, PlanThumbnailSize, File, FileLink, Plan


MODELS_TO_REGISTER = [
    UserProfile,
    ThumbnailSize,
    PlanThumbnailSize,
    File,
    FileLink
]

class ThumbnailSizeAdmin(admin.StackedInline): # styl wyświetlania ManyToMany
    model = PlanThumbnailSize
    extra = 1

class PlanAdmin(admin.ModelAdmin): # Dla strony admina, modelu plan, wyświetl to.
   inlines = [ThumbnailSizeAdmin,]

admin.site.register(Plan, PlanAdmin)

admin.site.register(MODELS_TO_REGISTER)
