import json
def test_view_startsite(client):
    response = client.get('/')

    assert response.status_code == 200
    assert json.loads(response.data) == dict(statuscode=200,
                                             content="# Startseite fuer Testdaten\n")

def test_view_directory(client, data_structure):
    response = client.get(data_structure[1]['path'])

    assert response.status_code == 400
    assert json.loads(response.data) == dict(statuscode=400,
                                             message="Der Pfad ist ungueltig")



#    print(data_structure[1])