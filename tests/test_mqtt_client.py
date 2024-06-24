import ssl

import pytest
from aiomqtt import ProtocolVersion

from bluetti_mqtt.mqtt_client import MQTTClient


@pytest.mark.parametrize("broker_url, expected", [
    ('mqtt://user:password@example.net:1883?client_id=dev', {
        'hostname': 'example.net',
        'port': 1883,
        'username': 'user',
        'password': 'password',
        'identifier': 'dev',
        'transport': 'tcp',
        'protocol': None,
        'tls_context': None,
        'tls_insecure': None,
    }),
    ('mqtts://example.net', {
        'port': 8883,
        'transport': 'tcp',
    }),
    ('ws://example.net', {
        'port': 80,
        'transport': 'websockets',
    }),
    ('wss://example.net', {
        'port': 443,
        'transport': 'websockets',
    }),
    ('mqtt://example.net?protocol=v31', {
        'protocol': ProtocolVersion.V31,
    }),
    ('mqtt://example.net?protocol=v311', {
        'protocol': ProtocolVersion.V311,
    }),
    ('mqtt://example.net?protocol=v5', {
        'protocol': ProtocolVersion.V5,
    }),
])
def test_parse_broker_url(broker_url: str, expected):
    got = MQTTClient.parse_broker_url(broker_url)
    for key, value in expected.items():
        assert got[key] == value


@pytest.mark.parametrize('tls_insecure, check_hostname, verify_mode', [
    (True, False, ssl.CERT_NONE),
    (False, True, ssl.CERT_REQUIRED),
])
def test_parse_broker_url_tls_insecure(tls_insecure: bool, check_hostname: bool, verify_mode: int):
    got = MQTTClient.parse_broker_url(f'mqtts://example.net?tls_insecure={tls_insecure}')
    ctx = got['tls_context']
    assert ctx.check_hostname is check_hostname
    assert ctx.verify_mode == verify_mode
