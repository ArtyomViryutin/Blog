import pytest


class TestUrls:
    @pytest.mark.django_db(transaction=True)
    def test_index_url(self, client, user_client):
        url = '/'
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница `{url}` работает неправильно. Ошибка: `{e}`'
        if response.status_code in (301, 302):
            response = client.get(url)
        assert response.status_code != 404, f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        try:
            response = user_client.get(url)
        except Exception as e:
            assert False, f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(url)
        assert response.status_code != 404, f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'

    @pytest.mark.django_db(transaction=True)
    def test_group_url(self, client, user_client, group):
        try:
            response = client.get(f'/group/{group.slug}')
        except Exception as e:
            assert False, f'''Страница `/group/<slug>/` работает неправильно. Ошибка: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'/group/{group.slug}/')
        assert response.status_code != 404, 'Страница `/group/<slug>/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, 'Страница `/group/<slug>/` работает неправильно.'

    # @pytest.mark.django_db(transaction=True)
    # def test_new_url(self, client, user_client):
    #     try:
    #         response = client.get('/new')
    #     except Exception as e:
    #         assert False, f'''Страница `/new` работает неправильно. Ошибка: `{e}`'''
    #     assert False, f'status code: {response.status_code}'


