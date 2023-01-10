from http import HTTPStatus

import pytest

from api.models import Indication, Station


@pytest.mark.django_db(transaction=True)
class TestStateAPI:
    state_url = '/api/v1/stations/{id}/state/'

    def check_state_data(self, response_data, url):
        response_state_fields = ('x', 'y', 'z')

        response_state_not_fields = (
            'id', 'name', 'condition', 'create_date', 'broken_date', 'user',
            'station_id', 'axis', 'distanse'
        )

        for field in response_state_fields:
            assert field in response_data, {
                  f'В ответе на {url} отсутствует поле {field}.'
            }

        for field in response_state_not_fields:
            assert field not in response_data, (
                f'В ответе на {url}'
                f'присутствует лишнее поле {field}.'
            )

    def test_state_get_unauth(self, client, station_1):
        response = client.get(self.state_url.format(id=station_1.id))

        assert response.status_code == HTTPStatus.OK, (
            'GET-запрос неавторизованного пользователя к '
            f'{self.state_url.format(id=station_1.id)} должен вернуть ответ '
            'со статусом 200.'
        )

    # параметризованный запрос для станции
    @pytest.mark.parametrize('distance', (200, -200))
    @pytest.mark.parametrize('axis', ('x', 'y', 'z'))
    def test_state_create_auth_with_valid_data(
        self, user_client, station_1, distance, axis
    ):
        data = {'axis': axis, 'distance': distance}
        distance_station = getattr(station_1, axis)

        indication_count = Indication.objects.count()

        response = user_client.post(
                self.state_url.format(id=station_1.id), data=data
            )

        assert response.status_code == HTTPStatus.CREATED, (
            'Для авторизованного пользователя POST-запрос с корректными'
            f'данными к {self.state_url.format(id=station_1.id)} '
            'должен вернуть ответ со статусом 201.'
        )

        indication_count += 1

        assert indication_count == Indication.objects.count(), (
            f'POST-запрос авторизованного пользователя к {self.state_url} '
            'должен создать новую запист в таблице с указаниями.'
        )

        data_state = response.json()
        station = Station.objects.get(id=station_1.id)


        assert isinstance(data_state, dict), (
            'POST-запрос авторизованного пользователя к '
            f'{self.state_url} не вернул ответ в виде словаря.'
        )

        self.check_state_data(
            data_state, f'POST-запрос к {self.state_url}'
        )

        assert data_state.get(axis) == distance + distance_station, (
            'POST-запрос авторизванного пользователя к '
            f'{self.state_url} должен вернуть ответ содержащий '
            f'поле {axis} c новым значением координаты.'
        )

        if data_state.get(axis) <= 0:
            assert station.condition == 'broken', (
                'Если в результате POST-запроса к '
                f'{self.state_url} координат {axis} <= 0 '
                'поле condition должно имет значение broken.'
            )

            assert station.broken_date, (
                'Если в результате POST-запроса к '
                f'{self.state_url} координат {axis} <= 0 '
                'поле broken_date должно быть заполнено.'
            )
        else:
            assert station.condition == station_1.condition, (
                'Если в результате POST-запроса к '
                f'{self.state_url} значение координаты {axis} положительно '
                'то значение поля condition не должно изменится.'
            )


    @pytest.mark.parametrize('axis', ('x', 'y', 'z'))
    def test_state_unauth_create(self, client, axis):

        distance = 200
        data = {'axis': axis, 'distance': distance}

        indication_count = Indication.objects.count()

        response = client.post(self.state_url, data=data)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'POST-запрос неавторизованного пользователя к '
            f'{self.state_url} должен вернуть ответ со статусом 401.'
        )

        assert indication_count == Indication.objects.count(), (
            'POST-запрос неавторизованного пользователя к '
            f'{self.state_url} не должен создавать новую запись в таблице.'
        )
