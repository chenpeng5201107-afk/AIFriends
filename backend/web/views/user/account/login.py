from rest_framework import authentication, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.modules.user import UserProfile


class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username').strip()
            password = request.data.get('password').strip()
            if not username or not password:
                return Response({'result':'用户名或密码不能为空~'})
            user = authentication.authenticate(username=username, password=password)
            if user: # 用户名密码正确
                user_profile = UserProfile.objects.get(username=username)
                refresh_token = RefreshToken.for_user(user) # 生成refresh_token
                response = Response({
                    'result':'登录成功~',
                    'access':str(refresh_token.access_token),
                    'user_id':user.id,
                    'photo':user_profile.photo.url,
                    'username':user.username,
                    'profile':user_profile.profile,
                    })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh_token),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=86400*7,
                )
                return  response
            return Response({'result':'用户名或密码错误~'})
        except:
            return Response({'result':'系统异常，请稍后尝试~'})