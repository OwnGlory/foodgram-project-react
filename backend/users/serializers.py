import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import MyUser
from subscribe.models import Subscribe


class UserListSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        model = MyUser

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user,
                                            author=obj).exists()
        return False


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            UniqueValidator(queryset=MyUser.objects.all()),
        )
    )
    email = serializers.EmailField(
        max_length=254,
        validators=(
            UniqueValidator(queryset=MyUser.objects.all()),
        )
    )

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name')
        model = MyUser

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать'
                                              'патерну ^[\\w.@+-]+\\Z')
        return value


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            UniqueValidator(queryset=MyUser.objects.all()),
        )
    )
    email = serializers.EmailField(
        max_length=254,
        validators=(
            UniqueValidator(queryset=MyUser.objects.all()),
        )
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        model = MyUser

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать'
                                              'патерну ^[\\w.@+-]+\\Z')
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError('Пароль не может быть пустым.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
