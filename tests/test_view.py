def test_startsite(client):
    response = client.get('/')

    assert response.status_code == 200

    print(response.data)

