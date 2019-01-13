from rest_framework import serializers
from . import models
from nomadgram.users import models as user_models


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image'
        )

class CommentSerializer(serializers.ModelSerializer):
    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator'
        )


class LikeSerializer(serializers.ModelSerializer):
    #image = ImageSerializer()

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'creator',            
            'created_at',
            'updated_at',
            'comments',
            'likes',
            'count_likes'
        )
