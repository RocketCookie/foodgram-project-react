from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, odj):
        request = self.context.get('request')
        user = self.context['request'].user

        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=user, author=odj).exists()
        return False
