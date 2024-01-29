from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from users.permissions import IsAdminOwnerOrReadOnly
from users.serializers import UserSerializer, UserListSerializer
from users.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MyUser.objects.all()
    permission_classes = (IsAdminOwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=id',)
    http_method_names = ('get', 'post')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        return UserSerializer

    @action(
        methods=(
            'get',
        ),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def users_own_profile(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        serializer = UserListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
