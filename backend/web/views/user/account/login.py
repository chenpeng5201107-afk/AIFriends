from rest_framework import authentication, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate  # 修改这里
from web.modules.user import UserProfile


class LoginView(APIView):
    def post(self, request):
        try:
            print("=" * 60)
            print("📥 收到登录请求")
            print(f"  - 请求数据: {request.data}")

            username = request.data.get('username')
            password = request.data.get('password')

            print(f"  - 用户名: {username}")
            print(f"  - 密码长度: {len(password) if password else 0}")

            if not username or not password:
                print("❌ 用户名或密码为空")
                return Response({'result': '用户名或密码不能为空~'})

            username = username.strip()
            password = password.strip()

            print(f"  - 清理后用户名: {username}")

            # 认证
            print("🔐 开始认证...")
            user = authenticate(request, username=username, password=password)
            print(f"  - 认证结果: {user}")

            if user:
                print(f"✅ 认证成功: {user.username} (ID: {user.id})")

                # 获取用户资料
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    print(f"  - 用户资料: {user_profile}")
                except UserProfile.DoesNotExist:
                    print("❌ 用户资料不存在")
                    return Response({'result': '用户资料不存在~'})

                # 生成 token
                refresh_token = RefreshToken.for_user(user)
                access_token = str(refresh_token.access_token)
                print(f"  - Access Token: {access_token[:20]}...")

                # 构建响应
                response_data = {
                    'result': '登录成功~',
                    'access': access_token,
                    'user_id': user.id,
                    'photo': user_profile.photo.url if user_profile.photo else '',
                    'username': user.username,
                    'profile': user_profile.profile,
                }

                print(f"📤 响应数据: {response_data}")
                print(f"  - 数据大小: {len(str(response_data))} 字节")

                response = Response(response_data)

                # 设置 cookie (开发环境 secure=False)
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh_token),
                    httponly=True,
                    secure=False,  # 开发环境用 False
                    samesite='Lax',
                    max_age=86400 * 7,
                )

                print("✅ 登录处理完成，返回响应")
                print("=" * 60)
                return response

            print("❌ 认证失败：用户名或密码错误")
            return Response({'result': '用户名或密码错误~'})

        except Exception as e:
            print("💥 系统异常:")
            import traceback
            traceback.print_exc()
            return Response({'result': f'系统异常，请稍后尝试~'})