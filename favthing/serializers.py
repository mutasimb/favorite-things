from rest_framework import serializers

from .models import FavThing


class FavThingSerializer(serializers.Serializer):
    pid = serializers.UUIDField(format='hex_verbose', read_only=True)
    title = serializers.CharField(max_length=60)
    description = serializers.CharField(min_length=10, allow_blank=True)
    category = serializers.CharField(max_length=60)
    ranking = serializers.IntegerField(min_value=0)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    meta = serializers.CharField()

    def create(self, validated_data):
        return FavThing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.ranking = validated_data.get('ranking', instance.ranking)
        instance.meta = validated_data.get('meta', instance.meta)

        instance.save()
        return instance


class RankingSerializer(serializers.Serializer):
    pid = serializers.UUIDField(format='hex_verbose', read_only=True)
    ranking = serializers.IntegerField(min_value=0)

    def update(self, instance, validated_data):
        instance.ranking = validated_data.get('ranking', instance.ranking)
        instance.save()
        return instance
