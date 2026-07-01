import os
import socket

import requests
from flask import Flask, render_template

app = Flask(__name__)

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')


def get_combined_metrics():
    try:
        backend_data = requests.get(f"{BACKEND_URL}/metrics", timeout=5).json()
    except requests.exceptions.ConnectionError:
        backend_data = {"error": "backend unreachable"}
    except requests.exceptions.Timeout:
        backend_data = {"error": "backend timed out"}
    except Exception as e:
        backend_data = {"error": str(e)}

    return {
        "web_server": os.environ.get('HOST_HOSTNAME', socket.gethostname()),
        "backend": backend_data,
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/metrics')
def metrics():
    return get_combined_metrics()


@app.route('/health')
def health():
    return {"status": "ok", }


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)
