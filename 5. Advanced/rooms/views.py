from django.conf import settings
from django.db import transaction
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)

from reviews.models import Review
from .models import Room, Amenity, Facility, HouseRule
from categories.models import Category
from .serializers import (
    RoomListSerializer,
    RoomDetailSerializer,
    AmenitySerializer,
    FacilitySerializer,
    HouseRuleSerializer,
)
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer, VideoSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        created_amenity = serializer.save()
        serializer = AmenitySerializer(created_amenity)
        return Response(serializer.data)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity_detail = self.get_object(pk)
        serializer = AmenitySerializer(amenity_detail)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity_detail = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity_detail,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        updated_amenity = serializer.save()
        serializer = AmenitySerializer(updated_amenity)
        return Response(serializer.data)

    def delete(self, request, pk):
        amenity_detail = self.get_object(pk)
        amenity_detail.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Facilities(APIView):
    def get(self, request):
        all_facilities = Facility.objects.all()
        serializer = FacilitySerializer(all_facilities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacilitySerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.errors)

        created_facility = serializer.save()
        serializer = FacilitySerializer(created_facility)
        return Response(serializer.data)


class FacilityDetail(APIView):
    def get_object(self, pk):
        try:
            return Facility.objects.get(pk=pk)
        except Facility.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        facility_detail = self.get_object(pk)
        serializer = FacilitySerializer(facility_detail)
        return Response(serializer.data)

    def put(self, request, pk):
        facility_detail = self.get_object(pk)
        serializer = FacilitySerializer(
            facility_detail,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        updated_facility = serializer.save()
        serializer = FacilitySerializer(updated_facility)
        return Response(serializer.data)

    def delete(self, request, pk):
        facility = self.get_object(pk)
        facility.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class HouseRules(APIView):
    def get(self, request):
        all_houserules = HouseRule.objects.all()
        serializer = HouseRuleSerializer(all_houserules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HouseRuleSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.errors)

        created_houserule = serializer.save()
        serializer = HouseRuleSerializer(created_houserule)
        return Response(serializer.data)


class HouseRuleDetail(APIView):
    def get_object(self, pk):
        try:
            return HouseRule.objects.get(pk=pk)
        except HouseRule.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        houserule_detail = self.get_object(pk)
        serializer = HouseRuleSerializer(houserule_detail)
        return Response(serializer.data)

    def put(self, request, pk):
        houserule_detail = self.get_object(pk)
        serializer = HouseRuleSerializer(
            houserule_detail,
            request.data,
            partial=True,
        )
        if serializer.is_valid():
            return Response(serializer.errors)

        updated_houserule = serializer.save()
        serializer = HouseRuleSerializer(updated_houserule)
        return Response(serializer.data)

    def delete(self, request, pk):
        houserule = self.get_object(pk)
        houserule.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        category_pk = request.data.get("category")
        if not category_pk:
            raise ParseError("Category is required.")

        try:
            category = Category.objects.get(pk=category_pk)
            if category.category_type == Category.CatogoryTypeChoices.EXPERIENCES:
                raise ParseError("The Category Type should be 'room'.")
        except Category.DoesNotExist:
            raise ParseError("Category not found.")

        with transaction.atomic():
            try:
                created_room = serializer.save(
                    host=request.user,
                    category=category,
                )
                amenities = request.data.get("amenities")

                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    created_room.amenities.add(amenity)
            except Exception:
                raise ParseError("Amenity not found.")

            try:
                facilities = request.data.get("facilities")
                for facility_pk in facilities:
                    facility = Facility.objects.get(pk=facility_pk)
                    created_room.facilities.add(facility)
            except Exception:
                raise ParseError("Facility not found.")

            try:
                house_rules = request.data.get("house_rules")
                for house_rule_pk in house_rules:
                    house_rule = HouseRule.objects.get(pk=house_rule_pk)
                    created_room.house_rules.add(house_rule)
            except Exception:
                raise ParseError("House Rule not found.")

            serializer = RoomDetailSerializer(
                created_room,
                context={"request": request},
            )
            return Response(serializer.data)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room_detail = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room_detail,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room_detail = self.get_object(pk)
        if room_detail.host != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            room_detail,
            request.data,
            partial=True,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(serializer.errors)

        category_pk = request.data.get("category")
        if not category_pk:
            raise ParseError("Category is required.")

        try:
            category = Category.objects.get(pk=category_pk)
            if category.category_type == Category.CatogoryTypeChoices.EXPERIENCES:
                raise ParseError("The Category Type should be 'room'.")
        except Category.DoesNotExist:
            raise ParseError("Category not found.")

        with transaction.atomic():
            try:
                updated_room = serializer.save(
                    host=request.user,
                    category=category,
                )
                amenities = request.data.get("amenities")

                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    updated_room.amenities.add(amenity)
            except Exception:
                raise ParseError("Amenity not found.")

            try:
                facilities = request.data.get("facilities")
                for facility_pk in facilities:
                    facility = Facility.objects.get(pk=facility_pk)
                    updated_room.facilities.add(facility)
            except Exception:
                raise ParseError("Facility not found.")

            try:
                house_rules = request.data.get("house_rules")
                for house_rule_pk in house_rules:
                    house_rule = HouseRule.objects.get(pk=house_rule_pk)
                    updated_room.house_rules.add(house_rule)
            except Exception:
                raise ParseError("House Rule not found.")

            serializer = RoomDetailSerializer(
                updated_room,
                context={"request": request},
            )
            return Response(serializer.data)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.host != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room_detail = self.get_object(pk)
        serialzer = ReviewSerializer(
            room_detail.reviews.all()[start:end],
            many=True,
        )
        return Response(serialzer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        created_review = serializer.save(
            user=request.user,
            room=self.get_object(pk),
        )
        serializer = ReviewSerializer(created_review)
        return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room_detail = self.get_object(pk)
        serialzer = AmenitySerializer(
            room_detail.amenities.all()[start:end],
            many=True,
        )
        return Response(serialzer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room_detail = self.get_object(pk)
        if room_detail.host != request.user:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.errors)

        created_photo = serializer.save(room=room_detail)
        serialzer = PhotoSerializer(created_photo)
        return Response(serialzer.data)
