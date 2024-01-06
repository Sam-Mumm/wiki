import json
import pytest
def test_view_startsite(client):
    response = client.get('/')

    assert response.status_code == 200
    assert json.loads(response.data) == dict(statuscode=200,
                                             content="# Startseite fuer Testdaten\n")


def test_view_content(client, testcase):
    response=client.get(testcase['context'])

    j=json.loads(response.data)

    assert response.status_code == testcase['response']['statuscode']
    assert j['statuscode'] == testcase['response']['json']['statuscode']

    #  Erwarten wir eine Fehlermeldung oder Inhalt?
    if 'content' in testcase['response']['json']:
        assert j['content'] == testcase['response']['json']['content']
    elif 'message' in testcase['response']['json']:
        assert j['message'] == testcase['response']['json']['message']
