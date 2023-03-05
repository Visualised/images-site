from django.test import TestCase
from django.urls import reverse
from .models import Plan, ThumbnailSize, PlanThumbnailSize, UserProfile, FileLink
from django.contrib.auth.models import User as DjangoUserModel
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        thumbnailsize_200x200 = ThumbnailSize.objects.create(name="200x200", width="200", height="200")
        thumbnailsize_400x400 = ThumbnailSize.objects.create(name="400x400", width="400", height="400")
        thumbnailsize_original = ThumbnailSize.objects.create(name="Original", width=None, height=None)
        thumbnailsize_binary = ThumbnailSize.objects.create(name="Binary", width=None, height=None)
        plan_basic = Plan.objects.create(plan="Basic", generate_binary_image=False)
        plan_enterprise = Plan.objects.create(plan="Enterprise", generate_binary_image=True)
        PlanThumbnailSize.objects.create(plan=plan_basic, size=thumbnailsize_200x200)
        PlanThumbnailSize.objects.create(plan=plan_enterprise, size=thumbnailsize_200x200)
        PlanThumbnailSize.objects.create(plan=plan_enterprise, size=thumbnailsize_400x400)
        PlanThumbnailSize.objects.create(plan=plan_enterprise, size=thumbnailsize_original)
        PlanThumbnailSize.objects.create(plan=plan_enterprise, size=thumbnailsize_binary)
        
    def setUp(self):
        self.user_basic = DjangoUserModel.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_basic_upload_image(self):
        basic_plan = Plan.objects.get(plan="Basic")
        UserProfile.objects.create(user=self.user_basic, plan=basic_plan)
        with open("gothic.jpg", "rb") as image:
            image_data = SimpleUploadedFile("gothic.jpg", image.read(), content_type="image/jpeg")
            self.client.post(reverse('images-app-upload'), {'file': image_data}, format="multipart")

        links = FileLink.objects.count()
        self.assertEquals(links, 1)

    def test_enterprise_no_binary(self):
        enterprise_plan = Plan.objects.get(plan="Enterprise")
        UserProfile.objects.create(user=self.user_basic, plan=enterprise_plan)
        with open("gothic.jpg", "rb") as image:
            image_data = SimpleUploadedFile("gothic.jpg", image.read(), content_type="image/jpeg")
            self.client.post(reverse('images-app-upload'), {'file': image_data}, format="multipart")

        links = FileLink.objects.count()
        self.assertEquals(links, 3)

    def test_enterprise_with_binary(self):
        enterprise_plan = Plan.objects.get(plan="Enterprise")
        UserProfile.objects.create(user=self.user_basic, plan=enterprise_plan)
        with open("gothic.jpg", "rb") as image:
            image_data = SimpleUploadedFile("gothic.jpg", image.read(), content_type="image/jpeg")
            self.client.post(reverse('images-app-upload'), {'file': image_data, "create_binary_image": True, "seconds_alive": 300}, format="multipart")

        links = FileLink.objects.count()
        self.assertEquals(links, 4)

    def tearDown(self):
        shutil.rmtree('uploads/testuser')