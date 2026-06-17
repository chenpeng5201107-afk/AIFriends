from rest_framework import response
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # 必须登录之后才可以访问
    def post(self, request):
        response = Response({'result':'退出登录成功~'})
        response.delete_cookie('refresh_token')
        return response