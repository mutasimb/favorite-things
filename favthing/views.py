import uuid
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin

from .models import FavThing
from .serializers import FavThingSerializer, RankingSerializer


class FavThingView(CsrfExemptMixin, APIView):
    authentication_classes = []

    def get(self, request):
        items = FavThing.objects.all()
        serializer = FavThingSerializer(items, many=True)
        return Response({"favorite_things": serializer.data})

    def post(self, request):
        req_category = request.data.get("category")
        req_ranking = request.data.get("ranking")

        serializer = FavThingSerializer(data=request.data)

        items_to_update = FavThing.objects.all().filter(
            category=req_category).filter(ranking__gte=req_ranking)

        if serializer.is_valid():
            for item in items_to_update:
                rank_serializer = RankingSerializer(
                    instance=item, data={
                        "ranking": item.ranking+1}, partial=True)
                if rank_serializer.is_valid():
                    item_updated = rank_serializer.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavThingDetail(CsrfExemptMixin, APIView):
    authentication_classes = []

    def get_object(self, pk):
        try:
            return FavThing.objects.get(pk=pk)
        except FavThing.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        item_to_delete = self.get_object(pk=pk)

        current_category = item_to_delete.category
        current_ranking = item_to_delete.ranking

        items_to_update = FavThing.objects.all().filter(
            category=current_category).filter(ranking__gt=current_ranking)

        item_to_delete.delete()
        for item in items_to_update:
            rank_serializer = RankingSerializer(
                instance=item, data={"ranking": item.ranking-1}, partial=True)
            if rank_serializer.is_valid():
                rank_serializer.save()
        return Response(
            {"success": "Favorite thing with id '{}' has been deleted.".format(
                pk)},
            status=204)

    def put(self, request, pk):
        item_to_put = self.get_object(pk=pk)

        current_category = item_to_put.category
        current_ranking = item_to_put.ranking
        req_category = request.data.get("category")
        req_ranking = request.data.get("ranking")

        if current_category != req_category:
            items_to_update_current = FavThing.objects.all().filter(
                category=current_category).filter(ranking__gt=current_ranking)
            items_to_update_req = FavThing.objects.all().filter(
                category=req_category).filter(ranking__gte=req_ranking)

            for item in items_to_update_current:
                current_serializer = RankingSerializer(
                    instance=item,
                    data={"ranking": item.ranking-1},
                    partial=True)
                if current_serializer.is_valid():
                    current_serializer.save()

            for item in items_to_update_req:
                req_serializer = RankingSerializer(
                    instance=item,
                    data={"ranking": item.ranking+1},
                    partial=True)
                if req_serializer.is_valid():
                    req_serializer.save()

        elif current_category == req_category:
            if req_ranking < current_ranking:
                items_to_update = FavThing.objects.all().filter(
                    category=req_category).filter(
                    ranking__gte=req_ranking).filter(
                    ranking__lt=current_ranking)

                for item in items_to_update:
                    rank_serializer = RankingSerializer(
                        instance=item,
                        data={"ranking": item.ranking+1},
                        partial=True)
                    if rank_serializer.is_valid():
                        rank_serializer.save()
            elif req_ranking > current_ranking:
                items_to_update = FavThing.objects.all().filter(
                    category=req_category).filter(
                    ranking__lte=req_ranking).filter(
                    ranking__gt=current_ranking)

                for item in items_to_update:
                    rank_serializer = RankingSerializer(
                        instance=item,
                        data={"ranking": item.ranking-1},
                        partial=True)
                    if rank_serializer.is_valid():
                        rank_serializer.save()

        serializer = FavThingSerializer(
            instance=item_to_put, data=request.data, partial=True)
        if serializer.is_valid():
            item_saved = serializer.save()
            return Response({
                "success": "Favorite thing '{}' updated successfully".format(
                    item_saved.title),
                "data": serializer.data})
        return Response({
            "failure": "Favorite thing '{}' failed to updated".format(
                item_saved.title),
            "data": serializer.data},
            status=status.HTTP_400_BAD_REQUEST)
