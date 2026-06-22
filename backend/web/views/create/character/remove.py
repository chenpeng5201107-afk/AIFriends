from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.modules.character import Character
from web.views.create import character
from web.views.utils.photo import remove_old_photo


class RemoveCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            character_id = request.data.get('character_id')
            Character.objects.filter(id=character_id,author__user = request.user).delete()
            return Response({
                'result': 'success'
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试~'
            })