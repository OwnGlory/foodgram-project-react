from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from subscribe.serializers import SubscribeSerializer
from subscribe.models import Subscribe
from users.models import MyUser


class SubscribeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = ('get', 'post', 'delete')
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.user.all()

    @action(
        methods=(
            'post',
            'delete',
        ),
        url_path='subscribe',
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(MyUser, id=pk)
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST)
            queryset = Subscribe.objects.create(author=author, user=user)
            serializer = SubscribeSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            subscribe = Subscribe.objects.filter(author=author, user=user)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
