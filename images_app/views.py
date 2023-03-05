from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import CanUploadFile
from .models import File, UserProfile, PlanThumbnailSize
from .serializers import FileSerializer, FileLinkSerializer, BinaryFileSerializer
from easy_thumbnails.files import get_thumbnailer
from .cron import housekeeping_job

class UploadFile(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, CanUploadFile]

    @staticmethod
    def fetch_available_thumbnail_types(user_plan):
        types = PlanThumbnailSize.objects.filter(plan=user_plan).select_related("size")
        return list(types)

    def perform_create(self, serializer):
        user = self.request.user
        user_plan = UserProfile.objects.get(user=user).plan
        file = serializer.save(user=user)

        thumbnail_types = self.fetch_available_thumbnail_types(user_plan)

        domain_url = self.request.build_absolute_uri('/')[:-1]

        for thumbnail_type in thumbnail_types:
            size = thumbnail_type.size
            name = thumbnail_type.size.name
            if size.width or size.height:
                options = {"size": (size.width, size.height)}
                thumb_url = domain_url + get_thumbnailer(file.file).get_thumbnail(options).url
            elif name == "Binary":
                thumb_url = file.binary_image
            else:
                thumb_url = domain_url + file.file.url 

            thumb_data = {
                "file": file.pk, 
                "link": thumb_url, 
                "thumbnail_type": size.pk,
                }
            
            file_link_serializer = FileLinkSerializer(data=thumb_data)
            if file_link_serializer.is_valid():
                file_link_serializer.save()
        
    def get_serializer_class(self):
        user = self.request.user
        user_plan = UserProfile.objects.get(user=user).plan
        if user_plan.generate_binary_image == True:
            return BinaryFileSerializer
        return FileSerializer


class ListFile(ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(user=user)
    
    def list(self, request):
        housekeeping_job()
        return super().list(self, request)