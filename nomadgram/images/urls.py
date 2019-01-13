from django.conf.urls import url
from . import views

app_name = "images"

urlpatterns = [
    url(
        regex=r'^$',
        view=views.Feed.as_view(),
        name='feed'
    ),
    url(# image_id : URL의 Variable
        regex=r'(?P<image_id>\w+)/likes/',
        view=views.LikeImage.as_view(),
        name='like_image'
    ),
    url(
        regex=r'(?P<image_id>\w+)/comments/',
        view=views.CommentOnImage.as_view(),
        name='comment_image'
    )
    #url(
    #    regex='^all/$',
    #    view=views.ListAllImages.as_view(),
    #    name='all_images'
    #),
    #url(
    #    regex='^comments/$',
    #    view=views.ListAllComments.as_view(),
    #    name='all_comments'
    #),
    #url(
    #    regex='^likes/$',
    #    view=views.ListAllLikes.as_view(),
    #    name='all_likes'
    #)
]