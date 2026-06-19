from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from web.modules.user import UserProfile


class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated] # 必须登录之后才可以访问
    def get(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            return Response({
                'result':'success',
                'username':user.username,
                'photo':user_profile.photo.url,
                'profile':user_profile.profile,
                'user_id':user.id
            })

        except:
            return Response({'result':'系统异常，请稍后尝试~'})

