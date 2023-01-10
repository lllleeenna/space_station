import pytest

from api.models import Station


@pytest.fixture
def station_1():
    return Station.objects.create(name='Станция 1')


@pytest.fixture
def station_2():
    return Station.objects.create(name='Станция 2')
