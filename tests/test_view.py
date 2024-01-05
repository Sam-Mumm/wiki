import json
import pytest
def test_view_startsite(client):
    response = client.get('/')

    assert response.status_code == 200
    assert json.loads(response.data) == dict(statuscode=200,
                                             content="# Startseite fuer Testdaten\n")

#def test_view_directory(client, data_structure):
#
#        response=client.get(t['context'])
#
#        j=json.loads(response.data)
#
#        assert response.status_code == t['response']['statuscode']
#        assert j['statuscode'] == t['response']['json']['statuscode']
#
#        #  Erwarten wir eine Fehlermeldung oder Inhalt?
#        if 'content' in t['response']['json']:
#            assert j['content'] == t['response']['json']['content']
#        elif 'message' in t['response']['json']:
#            assert j['message'] == t['response']['json']['message']

def test_example(client, testcase):
    response=client.get(testcase['context'])

    print(testcase)