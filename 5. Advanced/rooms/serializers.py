from rest_framework import serializers
from .models import Room, Amenity, Facility, HouseRule
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "name",
            "description",
        )


class HouseRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseRule
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):
    review_rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "review_rating",
            "is_host",
            "photos",
        )

    def get_review_rating(self, room):
        return room.review_rating()

    def get_is_host(self, room):
        request = self.context["request"]
        return room.host == request.user


class RoomDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    facilities = FacilitySerializer(read_only=True, many=True)
    house_rules = HouseRuleSerializer(read_only=True, many=True)
    review_rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_review_rating(self, room):
        return room.review_rating()

    def get_is_host(self, room):
        request = self.context["request"]
        return room.host == request.user
