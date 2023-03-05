from rest_framework import serializers
from datetime import datetime, timedelta
from .models import File, FileLink, ThumbnailSize, PlanThumbnailSize
import base64
import os
import magic

class FileSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)

    class Meta:
        model = File
        fields = ("id", "created_at", "file", "urls")

class BinaryFileSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)
    create_binary_image = serializers.BooleanField(write_only=True)
    seconds_alive = serializers.IntegerField(min_value=300, max_value=300000, required=False, write_only=True)

    class Meta:
        model = File
        fields = ("id", "created_at", "file", "urls", "create_binary_image", "seconds_alive")

    def create(self, validated_data):
        create_binary_image = validated_data.pop('create_binary_image')
        file = validated_data["file"]
        file_extension = file.name.split('.')[-1]
        if create_binary_image:
            seconds_alive = validated_data.pop('seconds_alive')
            expiration_date = datetime.now() + timedelta(seconds=seconds_alive)
            binary_image = f"data:image/{file_extension};base64,{base64.b64encode(file.read()).decode()}"
        else:
            expiration_date = None
            binary_image = None
        file_obj = File.objects.create(**validated_data, binary_image_expires_at=expiration_date, binary_image=binary_image)

        return file_obj
    
    def validate(self, data):
        file = data["file"]
        valid_mime_types = ["image/jpeg", "image/png"]
        file_mime_type = magic.from_buffer(file.read(1024), mime=True)
        if file_mime_type not in valid_mime_types:
            raise serializers.ValidationError('Unsupported file type.')
        valid_file_extensions = ['.jpg', ".jpeg", ".png"]
        ext = os.path.splitext(file.name)[1]
        if ext.lower() not in valid_file_extensions:
            raise serializers.ValidationError('Unacceptable file extension.')
        
        return data


class ThumbnailSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailSize
        fields = ("id", "name", "width", "height")

class PlanThumbnailSizeSerializer(serializers.ModelSerializer):
    size = ThumbnailSizeSerializer()

    class Meta:
        model = PlanThumbnailSize
        fields = ("id", "plan", "size")

class FileLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileLink
        fields = ("file", "link", "thumbnail_type")