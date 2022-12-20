from rest_framework import serializers

from .models import Indication, Station


class StationSerializer(serializers.ModelSerializer):
    """Сериализатор модели Станция."""

    class Meta:
        model = Station
        # fields = '__all__'
        exclude = ('x', 'y', 'z')
        read_only_fields = ('condition', 'broken_date')


class StationStateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Станция. Используется в /state."""
    class Meta:
        model = Station
        fields = ('x', 'y', 'z')


class IndicationSerializer(serializers.ModelSerializer):
    """Сериализер для модели Указание."""

    class Meta:
        model = Indication
        fields = '__all__'
        read_only_fields = ('station', 'user')
