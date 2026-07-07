from unittest.mock import patch
from app import get_combined_metrics


def test_combined_metrics_structure():
    fake_backend = {"hostname": "appserver", "cpu_percent": 10.0}
    with patch("app.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_backend
        data = get_combined_metrics()
        assert "web_server" in data
        assert "backend" in data
        assert data["backend"] == fake_backend
