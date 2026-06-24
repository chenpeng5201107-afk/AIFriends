from rest_framework.views import APIView
from rest_framework.response import Response
from web.modules.character import Character
from web.modules.user import UserProfile
from django.contrib.auth.models import User

class GetListView(APIView):
    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count'))
            user_id = int(request.query_params.get('user_id'))
            user = User.objects.get(id=user_id)
            user_profile = UserProfile.objects.get(user=user)
            character_rows = Character.objects.filter(
                author = user_profile
            ).order_by('-id')[items_count:items_count+20]
            characters = []
            for character in character_rows:
                author = character.author
                characters.append({
                    'id': character.id,
                    'name': character.name,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                    'profile': character.profile,
                    'author': {
                        'user_id': author.user_id,
                        'username': author.user.username,
                        'photo': author.photo.url,
                    }
                })
            return Response({
                'result': 'success',
                'characters': characters,
                'user_profile':{
                    'user_id': user.id,
                    'username': user.username,
                    'photo': user_profile.photo.url,
                    'profile': user_profile.profile,
                }
            })
        except Exception as e:
            # ✅ 打印详细错误信息
            print(f"错误类型: {type(e).__name__}")
            print(f"错误信息: {str(e)}")
            return Response({
                'result': '系统异常，请稍后重试~'
            })