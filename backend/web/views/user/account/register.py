from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.modules.user import UserProfile

class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username').strip()
            password = request.data.get('password').strip()
            if not username or not password:
                return Response({'result':'用户名或密码不能为空~'})
            if User.objects.filter(username=username).exists():
                return Response({'result':'用户名已存在~'})
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile.objects.create(user=user)
            refresh_token = RefreshToken.for_user(user)
            response = Response({
                'result': '注册成功~',
                'access': str(refresh_token.access_token),
                'user_id': user.id,
                'photo': user_profile.photo.url,
                'username': user.username,
                'profile': user_profile.profile,
            })
            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=86400 * 7,
            )
            return response
        except:
            return Response({'result':'系统异常，请稍后尝试~'})