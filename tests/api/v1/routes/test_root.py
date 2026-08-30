def test_raiz_de_la_version_de_api_actual_debe_retornar_200_ok(client):
    response = client.get('/api/v1/')

    assert response.status_code == 200
    assert response.get_json() == {
        'status': 'ok',
    }
