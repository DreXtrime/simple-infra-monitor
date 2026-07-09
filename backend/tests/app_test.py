from app import get_metrics


def test_get_metrics():
    data = get_metrics()
    assert "hostname" in data
    assert "os" in data
    assert "cpu_percent" in data
    assert "memory_percent" in data


def test_cpu_percent_is_valid():
    data = get_metrics()
    assert 0 <= data["cpu_percent"] <= 100


def test_memory_values_are_positive():
    data = get_metrics()
    assert data["memory_total_mb"] > 0
    assert data["memory_used_mb"] > 0


def test_api_metrics_endpoint(client):
    response = client.get('/api/metrics')
    assert response.status_code == 200


def test_prometheus_metrics_endpoint(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'app_cpu_usage_percent' in response.data


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'
