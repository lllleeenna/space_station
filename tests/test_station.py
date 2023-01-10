from http import HTTPStatus

import pytest

from api.models import Station


@pytest.mark.django_db(transaction=True)
class TestStationAPI:
    station_url = '/api/v1/stations/'
    station_detail_url = '/api/v1/stations/{id}/'
    VALID_DATA_NAME = {'name': 'Солярис-2'}

    def check_station_data(self, response_data, url):
        response_station_fields = (
            'id', 'name', 'condition', 'create_date', 'broken_date'
        )
        response_station_not_fields = ('x', 'y', 'z')

        for field in response_station_fields:
            assert field in response_data, (
                f'В ответе на {url} отсутствует поле {field}.'
            )

        for field in response_station_not_fields:
            assert field not in response_data, (
                f'В ответе на {url}'
                f'присутствует лишнее поле {field}.'
            )

    def test_station_list_not_found(self, client):
        response = client.get(self.station_url)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпойнт {self.station_url} не найден.'
        )

    def test_station_list_not_auth(self, client):
        response = client.get(self.station_url)

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'{self.station_url}  возвращает ответ со статусом 200.'
        )

    def test_station_detail_not_auth(self, client, station_1):
        response = client.get(self.station_detail_url.format(id=station_1.id))

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'{self.station_detail_url} возвращает ответ со статусом 200.'
        )

    def test_station_list_auth(self, user_client, station_1, station_2):
        response = user_client.get(self.station_url)

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос авторизованного пользователя к '
            f'{self.station_url} возвращает ответ со статусом 200.'
        )

        data = response.json()
        assert isinstance(data, list), (
            'GET-запрос авторизованного пользователя к '
            f'{self.station_url} не вернул список.'
        )

        assert len(data) == Station.objects.count(), (
            'GET-запрос авторизованного пользователя к '
            f'{self.station_url} вернул список не всех станций.'
        )

        self.check_station_data(data[0], f'GET-запрос к {self.station_url}')

    def test_station_create_auth_with_invalid_data(self, user_client):
        station_count = Station.objects.count()
        response = user_client.post(self.station_url, data={})

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Для авторизованного пользователя POST-запрос с '
            f'некорректными данными к {self.station_url}, '
            'должен вернуть ответ со статусом 400.'
        )

        assert station_count == Station.objects.count(), (
            'Для авторизованного пользователя POST-запрос с '
            f'некорректными данными к {self.station_url} '
            'не должен изменить количество станций.'
        )

    def test_station_create_auth_with_valid_data(self, user_client):
        station_count = Station.objects.count()
        data = {'name': 'Солярис'}
        response = user_client.post(self.station_url, data=data)

        assert response.status_code == HTTPStatus.CREATED, (
            'Для авторизованного пользователя POST-запрос с '
            f'корректными данными к {self.station_url}'
            'должен вернуть ответ со статусом 201.'
        )

        station_count += 1

        assert station_count == Station.objects.count(), (
            'POST-запрос авторизованного пользователя к '
            f'{self.station_url} создает новую станцию.'
        )
        
        data_station = response.json()

        assert isinstance(data_station, dict), (
            'POST-запрос авторизованного пользователя к '
            f'{self.station_url} не вернул ответ в виде словаря.'
        )

        self.check_station_data(
            data_station, f'POST-запрос к {self.station_url}'
        )

        assert data_station.get('name') == data.get('name'), (
            'POST-запрос авторизванного пользователя к '
            f'{self.station_url} должен вернуть ответ содержащий '
            'поле name c название станции.'
        )

        assert data_station.get('condition') == 'runing', (
            'POST-запрос авторизванного пользователя к '
            f'{self.station_url} должен вернуть ответ содержащий '
            'поле condition c состоянием станции по умолчанию.'
        )

        assert data_station.get('create_date'), (
            'POST-запрос авторизванного пользователя к '
            f'{self.station_url} должен вернуть ответ содержащий '
            'заполненное поле create_date.'
        )

        assert not data_station.get('broken_date'), (
            'POST-запрос авторизванного пользователя к '
            f'{self.station_url} должен вернуть ответ содержащий '
            'пустое поле broken_date.'
        )

        assert not data_station.get('x'), (
            'POST-запрос авторизванного пользователя к '
            f'{self.station_url} должен вернуть ответ, не содержащий поле x.'
        )

        assert not data_station.get('y'), (
            'POST-запрос авторизванного пользователя к '
            f'{self.station_url} должен вернуть ответ, не содержащий поле y.'
        )

        assert not data_station.get('z'), (
            'POST-запрос авторизванного пользователя к '
            f'{self.station_url} должен вернуть ответ, не содержащий поле z.'
        )

    def test_station_unauth_create(self, client):
        station_count = Station.objects.count()
        data = {'name': 'Солярис'}
        response = client.post(self.station_url, data=data)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'POST-запрос неавторизованного пользователя к '
            f'{self.station_url} должен вернуть ответ со статусом 401.'
        )

        assert station_count == Station.objects.count(), (
            'POST-запрос неавторизованного пользователя к '
            f'{self.station_url} не должен создавать новую станцию.'
        )

    def test_station_detail_auth(self, user_client, station_1):
        response = user_client.get(
            self.station_detail_url.format(id=station_1.id)
        )

        assert response.status_code == HTTPStatus.OK, (
            'GET-запрос к авторизованного пользователя к '
            f'{self.station_detail_url} должен вернуть статус 200.'
        )

        data = response.json()
        self.check_station_data(
            data, f'GET-запрос к {self.station_detail_url}'
        )

    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_station_detail_auth_valid_data(
        self, user_client, station_1, http_method
    ):
        request_func = getattr(user_client, http_method)
        print(request_func, '-' * 20)
        response = request_func(
            self.station_detail_url.format(id=station_1.id),
            data=self.VALID_DATA_NAME
        )

        assert response.status_code == HTTPStatus.OK, (
            f'{http_method.upper()}-запрос авторизованного пользователя к '
            f'{self.station_detail_url} должен вернуть ответ со статусом 200.'
        )

        station_test = Station.objects.filter(id=station_1.id).first()

        assert station_test.name == self.VALID_DATA_NAME.get('name'), (
            f'{http_method.upper()}-запрос авторизованного пользователя к '
            f'{self.station_detail_url} должен изменить имя станции.'
        )

        data = response.json()
        self.check_station_data(
            data, f'{http_method.upper()}-запрос к {self.station_detail_url}')

    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_station_change_unauth_with_valid_data(
        self, client, station_1, http_method
    ):
        request_func = getattr(client, http_method)
        response = request_func(
            self.station_detail_url.format(id=station_1.id),
            data=self.VALID_DATA_NAME
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'{http_method.upper()}-запрос неавторизованного пользователя к '
            f'{self.station_detail_url} должен вернуть ответ со статусом 401.'
        )

        station_test = Station.objects.filter(id=station_1.id).first()
        assert station_test.name != self.VALID_DATA_NAME.get('name'), (
            f'{http_method.upper()}-запрос неавторизованного пользователя к '
            f'{self.station_detail_url} не должен изменить имя станции.'
        )

    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_station_patch_auth_with_invalid_data(
        self, user_client, station_1, http_method
    ):
        request_func = getattr(user_client, http_method)
        response = request_func(
            self.station_detail_url.format(id=station_1.id),
            data={'name': {}},
            format='json'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'{http_method.upper()}-запрос с некорректными данными от '
            f'авторизованного пользователя к {self.station_detail_url} '
            'возвращает ответ с кодом 400.'
        )

    def test_station_delete_by_auth(self, user_client, station_1):
        response = user_client.delete(
            self.station_detail_url.format(id=station_1.id)
        )

        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'DELETE-запрос авторизованного пользователя к '
            f'{self.station_detail_url} должен удалить станцию.'
        )

    def test_station_unauth_delete(self, client, station_1):
        response = client.delete(
            self.station_detail_url.format(id=station_1.id)
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'DELETE-запрос неавторизованного пользователя к'
            f'{self.station_detail_url} должен вернуть ответ со статусом 401.'
        )

        station_test = Station.objects.filter(id=station_1.id).first()

        assert station_test, (
            'DELETE-запрос неавторизованного пользователя к'
            f'{self.station_detail_url} не должен удаляет станцию.'
        )
