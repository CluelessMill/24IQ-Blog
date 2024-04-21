from os import makedirs, path, remove
from shutil import copyfileobj

from rest_framework import serializers

from .models import News, NewsComments, Sessions, User
from .utils.cript_utils import encrypt, hash_password


class NewsSerializer(serializers.Serializer):
    title = serializers.CharField()
    content_text = serializers.CharField()
    category = serializers.CharField()
    main_img = serializers.ImageField()
    logo_img = serializers.ImageField()
    creation_date = serializers.DateTimeField(
        input_formats=["iso-8601"], required=False
    )

    def create(self, validated_data):
        creation_date = validated_data.pop("creation_date", None)
        news_instance = News.objects.create(
            **validated_data, creation_date=creation_date
        )
        folder_name = str(news_instance.news_id)
        image_path = path.join("media", "news-images", folder_name)
        makedirs(name=image_path, exist_ok=True)
        self.move_uploaded_file(
            uploaded_file=news_instance.logo_img,
            destination_path=path.join(image_path, "logo-img.jpg"),
        )
        self.move_uploaded_file(
            uploaded_file=news_instance.main_img,
            destination_path=path.join(image_path, "main-img.jpg"),
        )
        news_instance.logo_img.name = path.join(
            "news-images", folder_name, "logo-img.jpg"
        )
        news_instance.main_img.name = path.join(
            "news-images", folder_name, "main-img.jpg"
        )
        news_instance.save()
        return news_instance

    def move_uploaded_file(self, uploaded_file, destination_path):
        with open(file=uploaded_file.path, mode="rb") as source:
            with open(file=destination_path, mode="wb") as destination:
                copyfileobj(fsrc=source, fdst=destination)
        remove(path=uploaded_file.path)


class NewsCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsComments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        validated_data["nickname"] = encrypt(data=validated_data["nickname"])
        validated_data["email"] = encrypt(data=validated_data["email"])
        validated_data["password"] = hash_password(password=validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = "__all__"


class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = "__all__"
