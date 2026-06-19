from cmath import exp

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from backend import settings


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({'result':'refresh_token不存在~'})
            refresh = RefreshToken(refresh_token)
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']: # 是否开启refresh_token的轮转
                refresh.set_jti()
                response = Response({
                    'result':'登录成功~',
                    'access':str(refresh.access_token),
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
            return Response({
                'result':'登录成功~',
                'access':str(refresh.access_token),
            })
        except:
            return Response({'result':'refresh_tokrn过期了~'},status=401)