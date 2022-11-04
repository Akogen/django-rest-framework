from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    category_type = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.category_type = validated_data.get(
            "category_type", instance.category_type
        )
        instance.save()
        return instance
