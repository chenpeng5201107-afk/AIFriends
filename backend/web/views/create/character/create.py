from django.db.models import Model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.modules.character import Character
from web.modules.user import UserProfile


class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user  = request.user
            user_profile = UserProfile.objects.get(user=user)
            name = request.data.get('name', '').strip()
            photo = request.FILES.get('photo', None)
            profile = request.data.get('profile', '').strip()[:100000]
            background_image = request.FILES.get('background_image', None)
            if not name:
                return Response({
                    'result': '角色名不能为空'
                })
            if not profile:
                return Response({
                    'result': '角色简介不能为空'
                })
            if not photo:
                return Response({
                    'result': '角色头像不能为空'
                })
            if not background_image:
                return Response({
                    'result': '角色背景图不能为空'
                })
            Character.objects.create(
                author=user_profile,
                name=name,
                photo=photo,
                profile=profile,
                background_image=background_image
            )
            return Response({
                'result': 'success'
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试~'
            })