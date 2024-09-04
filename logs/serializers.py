from authentication.models import CustomUser
from logs.models import Action, UserAction
from rest_framework import serializers

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class CustomUserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username')

class UserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAction
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = CustomUserLightSerializer(instance.user).data
        data["action"] = ActionSerializer(instance.action).data
        return data