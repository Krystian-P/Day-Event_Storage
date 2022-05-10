import unittest
import json
import pytest

from app import app

# Keep Id of document created by test_postDate(), and transfer to test_postDate()
@pytest.fixture(scope="session")
def context():
    return {}

# GET /dates test
def test_allData():
    response = app.test_client().get('/dates')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is list
    assert type(res[0]) is dict
    assert type(res[0]['month']) is str
    assert type(res[0]['day']) is int
    assert response.status_code == 200

# GET /popular test
def test_popularMonths():
    response = app.test_client().get('/popular')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res) is list
    assert type(res[0]) is dict
    assert type(res[0]['_id']) is str
    assert type(res[0]['days_checked']) is int
    assert response.status_code == 200

#Post /dates test
def test_postDate(context):
    response = app.test_client().post("/dates", json={
        "month": 2,
        "day": 20
    })
    res = json.loads(response.data.decode('utf-8'))
    context['response'] = res['_id']
    assert type(res) is dict
    assert type(res['day']) is int
    assert type(res['month']) is str
    assert type(res['text']) is str
    assert response.status_code == 201

# DELETE /dates/{id} test
def test_delDate(context):
    response = app.test_client().delete(f"/dates/{context.get('response')}", headers={"X-API-KEY": "BASIC_KEY"})
    assert response.status_code == 204


if __name__ == '__main__':
    unittest.main()
