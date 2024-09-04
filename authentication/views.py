from .serializers import UserSerializer
from authentication.models import CustomUser
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework import viewsets  
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken
from knox.settings import CONSTANTS
from rest_framework.permissions import IsAuthenticated

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
    
class ListTokensView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        tokens = AuthToken.objects.filter(user=user)
        token_list = []

        for token in tokens:
            token_list.append({
                'token_key': token.token_key,
                'expiry': token.expiry,
                'created': token.created,
            })

        return Response(token_list)

class DeleteTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        token_key = request.data.get('token_key', None)

        if token_key:
            tokens = AuthToken.objects.filter(token_key=token_key, user=request.user)
            if tokens.exists():
                tokens.delete()
                return Response({'detail': 'Token deleted successfully'}, status=200)
            else:
                return Response({'detail': 'Token not found'}, status=404)
        else:
            return Response({'detail': 'Token key not provided'}, status=400)


class MeAPI(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all().prefetch_related('groups', 'groups_menus','permissions', 'menus','menus__groups','menus__auth')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
