def test_startsite(client, data_structure):
    response = client.get('/')

#    print(data_structure)

    assert response.status_code == 200

    print(response.data)

