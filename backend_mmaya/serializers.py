from rest_framework import serializers

class BaseCrudSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        created_by = self.context['request'].user
        instance = self.Meta.model.objects.create(**validated_data, created_by=created_by)
        return instance
    
    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        updated_by = self.context['request'].user
        instance.updated_by = updated_by
        instance.save()
        return instance