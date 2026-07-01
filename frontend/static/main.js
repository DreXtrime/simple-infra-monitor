const REFRESH_INTERVAL = 5000;

let isPaused = false;
let intervalId = null;

const countdownCircle = document.getElementById("countdown-circle");
const countdownRing = document.getElementById("countdown-ring");
const pauseBtn = document.getElementById("pause-btn");
const refreshStatus = document.getElementById("refresh-status");

function updateElement(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

function fetchMetrics() {
    fetch("/metrics")
        .then(res => res.json())
        .then(data => {
            updateElement("web-server-hostname", data.web_server);
            if (data.backend.error) {
                ["hostname", "os", "os-version", "platform",
                    "cpu-percent", "cpu-count", "memory-percent",
                    "memory-used", "memory-total"].forEach(id => {
                    updateElement(id, "unavailable");
                });
                refreshStatus.textContent = `Backend error: ${data.backend.error}`;
                refreshStatus.classList.add("error");
                return;
            } else {
                refreshStatus.textContent = "Refreshing";
                refreshStatus.classList.remove("error");
            }
            updateElement("hostname", data.backend.hostname);
            updateElement("os", data.backend.os);
            updateElement("os-version", data.backend.os_version);
            updateElement("platform", data.backend.platform);
            updateElement("cpu-percent", data.backend.cpu_percent + "%");
            updateElement("cpu-count", data.backend.cpu_count);
            updateElement("memory-percent", data.backend.memory_percent + "%");
            updateElement("memory-used", data.backend.memory_used_mb + " MB");
            updateElement("memory-total", data.backend.memory_total_mb + " MB");
        })
        .catch(err => {
            refreshStatus.textContent = "Error fetching metrics";
            console.error(err);
        });
    startCountdown()
}

function startCountdown() {
    const start = Date.now();
    countdownCircle.setAttribute("stroke-dashoffset", "0");

    if (window.countdownTimer) clearInterval(window.countdownTimer);

    window.countdownTimer = setInterval(() => {
        const elapsed = Date.now() - start;
        const progress = Math.min(elapsed / (REFRESH_INTERVAL - 700), 1);
        countdownCircle.setAttribute("stroke-dashoffset", progress * 100);
    }, 100);
}

function startRefresh() {
    fetchMetrics();
    intervalId = setInterval(fetchMetrics, REFRESH_INTERVAL);
    refreshStatus.textContent = "Refreshing...";
    refreshStatus.classList.remove("paused");
    refreshStatus.classList.remove("error");
    countdownRing.classList.remove("paused");
}

function stopRefresh() {
    clearInterval(intervalId);
    clearInterval(window.countdownTimer);
    refreshStatus.textContent = "Paused";
    refreshStatus.classList.add("paused");
    countdownRing.classList.add("paused");
}

pauseBtn.addEventListener("click", () => {
    isPaused = !isPaused;
    pauseBtn.textContent = isPaused ? "Resume" : "Pause";
    isPaused ? stopRefresh() : startRefresh();
});

startRefresh();