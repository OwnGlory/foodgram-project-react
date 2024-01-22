from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from users.serializers import UserSerializer
from users.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=id',)
    http_method_names = ('get', 'post')

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
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
