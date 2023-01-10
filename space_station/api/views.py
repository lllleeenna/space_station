import datetime

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Station, User
from .serializers import (IndicationSerializer, StationSerializer,
                          StationStateSerializer)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    @extend_schema(methods=['GET'], responses=StationStateSerializer)
    @extend_schema(
        methods=['POST'],
        request=IndicationSerializer,
        responses=StationStateSerializer
    )
    @action(methods=['get', 'post'], detail=True)
    def state(self, request, pk=None):
        station = get_object_or_404(Station, pk=pk)

        if request.method == 'POST':
            serializer = IndicationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    station=station,
                    user=get_object_or_404(User, username=self.request.user)
                )
                distance = serializer.validated_data.get('distance')
                axis = serializer.validated_data.get('axis')
                if hasattr(station, axis):
                    setattr(station, axis, getattr(station, axis) + distance)
                if station.condition != 'broken' and getattr(station, axis) <= 0:
                    station.condition = 'broken'
                    station.broken_date = datetime.datetime.now()
                station.save()
                return Response(
                    StationStateSerializer(station).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            StationStateSerializer(station).data, status=status.HTTP_200_OK
        )
