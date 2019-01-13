from django.db import models
from nomadgram.users import models as user_models
from taggit.managers import TaggableManager


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)   # 모델이 추가 될 때 자동으로 시간 추가
    updated_at = models.DateTimeField(auto_now=True)       # 모델이 갱신 될 때 자동으로 시간 업데이트
   
    # 메타 클래스를 추가함으로써 abstract model이라고 장고에게 알려줌
    # abstract base 클래스는 데이터베이스와 연결되지 않음 (abstrct base 클래스는 데이터베이스를 생성하기 위해 사용하지 않음)
    class Meta:
        abstract = True

class Image(TimeStampedModel):
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True, related_name='images', on_delete=models.SET_NULL)
    tags = TaggableManager()

    # @property는 모델의 필드인데 데이터로 가지는 않지만 모델 안에 존재함
    # property는 function임
    # 자신의 이미지에 접근하므로 self
    @property
    def count_likes(self):
        return self.likes.all().count()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '{}-{}'.format(self.location, self.caption)


class Comment(TimeStampedModel):
    """ Comment Model """
    message = models.TextField()
    # 댓글 단 사람 (1명의 유저는 많은 댓글을 갖을 수 있음)
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL)
    # 댓글이 달린 이미지
    image = models.ForeignKey(Image, null=True, related_name='comments', on_delete=models.SET_NULL)

    def __str__(self):
        return self.message


class Like(TimeStampedModel):
    """ Like Model """
    # 좋아요를 누른 사람
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL)
    # 좋아요를 받은 이미지
    image = models.ForeignKey(Image, null=True, related_name='likes', on_delete=models.SET_NULL)

    def __str__(self):
        return '{} - Image Caption:{}'.format(self.creator, self.image.caption)
