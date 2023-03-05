import os
import magic
from rest_framework import serializers

def validate_is_jpeg_or_png(file):
    valid_mime_types = ["image/jpeg", "image/png"]
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise serializers.ValidationError('Unsupported file type.')
    valid_file_extensions = ['.jpg', ".jpeg", ".png"]
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise serializers.ValidationError('Unacceptable file extension.')
    
    return file

class ImageSerializer(serializers.ModelSerializer):
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