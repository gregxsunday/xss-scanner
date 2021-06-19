from re import L
import pytest
from flask import url_for

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def send_payload(client, payload):
    resp = client.get(f'/?name={payload}')
    return resp

def test_input_tag(client):
    resp = client.get(f'/?name=<input>asd</input>')
    assert resp.status_code == 200

def test_onclick(client):
    resp = send_payload(client, '<input onclick=alert()>asd</input>')
    assert resp.status_code == 403

def test_onmouse(client):
    resp = send_payload(client, '<input onmouseover=alert()>asd</input>')
    assert resp.status_code == 403

def test_onload(client):
    resp = send_payload(client, '<input onload=alert()>asd</input>')
    assert resp.status_code == 403

def test_onfocus(client):
    resp = send_payload(client, '<input onfocusin=alert()>asd</input>')
    assert resp.status_code == 403

def test_onpointer(client):
    resp = send_payload(client, '<input onpointerenter=alert(1)>')
    assert resp.status_code == 200

def test_script(client):
    resp = send_payload(client, '<script>')
    assert resp.status_code == 403

def test_img(client):
    resp = send_payload(client, '<img src=x>')
    assert resp.status_code == 403

def test_a(client):
    resp = send_payload(client, '<a href=asd>')
    assert resp.status_code == 403


def test_body(client):
    resp = send_payload(client, '<body>')
    assert resp.status_code == 403
