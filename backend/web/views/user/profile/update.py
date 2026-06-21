from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from web.modules.user import UserProfile
from web.views.utils.photo import remove_old_photo
from django.contrib.auth.models import User
import traceback


class updateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("\n" + "=" * 60)
        print("🚀 收到更新请求")
        print("=" * 60)

        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            username = request.data.get('username', '').strip()
            profile = request.data.get('profile', '').strip()[:500]
            photo = request.FILES.get('photo', None)

            print(f"👤 用户: {user.username} (ID: {user.id})")
            print(f"📝 新用户名: '{username}'")
            print(f"📝 新简介: '{profile[:30]}...'")
            print(f"📸 新头像: {photo.name if photo else 'None'}")

            if not username:
                print("❌ 用户名为空")
                return Response({
                    'result': '用户名不能为空'
                })
            if not profile:
                print("❌ 简介为空")
                return Response({
                    'result': '简介不能为空'
                })

            # ✅ 使用 User 模型检查用户名是否被占用
            if username != user.username:
                print(f"🔍 检查用户名 '{username}' 是否被占用...")
                if User.objects.filter(username=username).exists():
                    print(f"❌ 用户名 '{username}' 已被占用")
                    return Response({
                        'result': '用户名已存在'
                    })
                print(f"✅ 用户名 '{username}' 可用")

            if photo:
                print(f"📸 更新头像: {photo.name}")
                remove_old_photo(user_profile.photo)
                user_profile.photo = photo

            print(f"📝 更新简介: {profile[:30]}...")
            user_profile.profile = profile
            user_profile.update_time = now()
            user_profile.save()
            print("✅ UserProfile 保存成功")

            print(f"📝 更新用户名: {user.username} -> {username}")
            user.username = username
            user.save()
            print("✅ User 保存成功")

            response_data = {
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'profile': user_profile.profile,
                'photo': user_profile.photo.url if user_profile.photo else None,
            }
            print(f"📤 返回: {response_data}")
            print("=" * 60)

            return Response(response_data)

        except Exception as e:
            print("\n" + "=" * 60)
            print("❌❌❌ 发生异常 ❌❌❌")
            print("=" * 60)
            print(f"异常类型: {type(e).__name__}")
            print(f"异常信息: {str(e)}")
            print("\n完整堆栈:")
            traceback.print_exc()
            print("=" * 60)

            return Response({
                'result': '系统异常，请稍后重试~'
            })