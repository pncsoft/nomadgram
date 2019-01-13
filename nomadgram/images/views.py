from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

class Feed(APIView):
    def get(self, request, format=None):
        user = request.user
        print("### user : ", user)
        
        following_users = user.following.all()
        print("### following_users : ", following_users)

        image_list = []
        for following_user in following_users:
            print("### following_user : ", following_user)
            print("### following_user.gender : ", following_user.gender)
            # 리스트를 2개까지 제한
            print("### following_user.images.all()[:2] : ", following_user.images.all()[:2])

            user_images = following_user.images.all()[:2]
            for image in user_images:
                image_list.append(image)
        
        print("### image_list : ", image_list)
        
        # sorted 함수는 3개의 파라미터를 정의 할 수 있음
        # 1번째 : 어느 리스트를 정렬 할 것인가
        # 2번째 : 어떻게 정렬 할 것인가 - 길이기준? 이름기준? .. - 여기서는 오브젝트 기준이므로 key를 줘야 함
        # 3번째 : [옵션] reverse (orderby)
        # 2-1번째 : key는 function을 불러옴 - key가 호출한 함수의 리턴값을 기준으로 파이썬이 데이터 정렬함
        # 람다 함수 사용해도 됨 --> sorted_list = sorted(image_list, key=lambda x: x.created_at)
        sorted_list = sorted(image_list, key=get_key, reverse=True)
        
        print("### sorted_list : ", sorted_list)
        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(data=serializer.data)
    
    
def get_key(image):
    return image.created_at


class LikeImage(APIView):
    def get(self, request, image_id, format=None):

        user = request.user
        print("### user : ", user)

        try:
            found_image = models.Image.objects.get(id=image_id)
            print("### found_image : ", found_image)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            preexisting_like = models.Like.objects.get(
                creator = user,
                image = found_image
            )
            preexisting_like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator = user,
                image = found_image
            )
            new_like.save()

            return Response(status=status.HTTP_201_CREATED)


class CommentOnImage(APIView):
    def post(self, request, image_id, format=None):
        print("### request.data : ", request.data)

        user = request.user
        print("### user : ", user)

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            print("### it is valid")
            serializer.save(creator=user, image=found_image)

            print("### serializer : ", serializer)
            print("")
            print("### serializer.data : ", serializer.data)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("### it is not valid")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(status=200)


'''
# Create your views here.
class ListAllImages(APIView):

    # self : 이미 정의된 variable
    # # request : 클라이언트가 오브젝트 요청
    # # format : json, xml등이 될 수 있는데, 여기서는 디폴트 none으로 지정   -> 지정되어 있지 않으면 디폴트로 JSON 포맷으로 응답함
    def get(self, request, format=None):

        # 모델 안에 있는 모든 오브젝트 종류의 이미지를 가져오기
        all_images = models.Image.objects.all()

        # many=True : 이미지 한 개가 아니고 여러개를 시리얼라이징 할거라고 알려줌
        serializer = serializers.ImageSerializer(all_images, many=True)

        # 모든 엘리먼트를 시리얼라이즈 하면 이를 data variable로 저장함
        return Response(data=serializer.data)


class ListAllComments(APIView):

    def get(self, request, format=None):

        userid = request.user.id
        print("### userid : ", request.user.id)

        all_comments = models.Comment.objects.filter(creator=userid)

        serializer = serializers.CommentSerializer(all_comments, many=True)

        return Response(data=serializer.data)


class ListAllLikes(APIView):

    def get(self, request, format=None):

        all_likes = models.Like.objects.all()

        serializer = serializers.LikeSerializer(all_likes, many=True)

        return Response(data=serializer.data)
'''