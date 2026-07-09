import socket
import platform
import os
import psutil
from flask import Flask, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge, Counter, Info

app = Flask(__name__)

app_info = Info('app', 'Application information')
app_info.info({
    'hostname': os.environ.get('HOST_HOSTNAME', socket.gethostname()),
    'os': platform.system(),
    'os_version': platform.version(),
    'platform': platform.platform(),
})

cpu_gauge = Gauge('app_cpu_usage_percent', 'Current CPU usage percent')
memory_gauge = Gauge('app_memory_usage_percent', 'Current memory usage percent')
memory_used_gauge = Gauge('app_memory_used_mb', 'Memory used in MB')
memory_total_gauge = Gauge('app_memory_total_mb', 'Total memory in MB')
request_counter = Counter('app_http_requests_total', 'Total HTTP requests', ['endpoint'])
error_counter = Counter('app_http_errors_total', 'Total HTTP errors', ['endpoint', 'status_code'])


def get_metrics():
    return {
        'hostname': os.environ.get('HOST_HOSTNAME', socket.gethostname()),
        'os': platform.system(),
        'os_version': platform.version(),
        'platform': platform.platform(),
        'cpu_percent': psutil.cpu_percent(interval=0.5),
        'cpu_count': psutil.cpu_count(),
        'memory_percent': psutil.virtual_memory().percent,
        'memory_total_mb': round(psutil.virtual_memory().total / (1024 * 1024), 2),
        'memory_used_mb': round(psutil.virtual_memory().used / (1024 * 1024), 2),
    }


@app.route('/api/metrics')
def api_metrics():
    request_counter.labels(endpoint='/api/metrics').inc()
    return get_metrics()


@app.route('/metrics')
def prometheus_metrics():
    request_counter.labels(endpoint='/metrics').inc()
    try:
        data = get_metrics()
        cpu_gauge.set(data['cpu_percent'])
        memory_gauge.set(data['memory_percent'])
        memory_used_gauge.set(data['memory_used_mb'])
        memory_total_gauge.set(data['memory_total_mb'])
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    except Exception as e:
        error_counter.labels(endpoint='/metrics', status_code='500').inc()
        return {'error': str(e)}, 500


@app.route('/health')
def health():
    request_counter.labels(endpoint='/health').inc()
    return {'status': 'ok'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')  # nosec B104
    app.run(host=host, port=port)
