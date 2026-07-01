import socket
import platform
import os

import psutil
from flask import Flask

app = Flask(__name__)


def get_metrics():
    return {
        "hostname": os.environ.get('HOST_HOSTNAME', socket.gethostname()),
        "os": platform.system(),
        "os_version": platform.version(),
        "platform": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "cpu_count": psutil.cpu_count(),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_total_mb": round(psutil.virtual_memory().total / (1024 * 1024), 2),
        "memory_used_mb": round(psutil.virtual_memory().used / (1024 * 1024), 2),
    }


@app.route("/metrics")
def metrics():
    return get_metrics()


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port)
