# Real-Time Network Data Analyzer

## Overview
This project is a real-time network monitoring system that provides visibility into:
- Process-level network activity (PID → Application)
- RX / TX byte usage per application
- Active network connections
- Reverse DNS mapping (IP → Hostname)
- Real-time visualization using Grafana dashboards

---

# System Requirements

- Linux (Ubuntu recommended)
- Python 3.8+
- Docker & Docker Compose
- Prometheus (manual install required)

---

# 1. Install Prometheus (Manual)

Download from:
https://prometheus.io/download/

Extract:
```bash
tar -xvzf prometheus-*.tar.gz
```

Move into project directory:
```bash
mv prometheus-* network-analyzer/
```

Expected structure:
network-analyzer/

├── prometheus-*/

├── prometheus.yml

---

# 2. Python Virtual Environment Setup

Install venv:
```bash
sudo apt update
sudo apt install python3-venv -y
```

Create venv:
```bash
python3 -m venv .venv
```

Activate venv:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

# 3. Run the System

Start everything:
```bash
./start.sh
```

---

# What start.sh does
- Starts Grafana (Docker)
- Starts Prometheus
- Starts Python exporter

---

# Access URLs

Grafana:
http://localhost:3000
(admin / admin)

Prometheus:
http://localhost:9090

Metrics:
http://localhost:8000/metrics

---

# If grafana panel shows no data
 - Please click on 3 dots at the top left corner of a panel.
 - Click refresh
 - Click back to dashboard

# Project Structure

network-analyzer/

├── app_net_exporter.py

├── docker-compose.yml

├── prometheus.yml

├── start.sh

├── requirements.txt

├── grafana/

│   ├── provisioning/

│   └── dashboards/

│   └──└── network-dashboard.json

├── prometheus-*/

├── .venv/

---

# Features

- Real-time process network tracking
- RX/TX monitoring per application
- Active connection tracking
- Reverse DNS (IP → hostname)
- Grafana visualization dashboards

---

# Important Notes

- Prometheus must be installed manually
- Virtual environment must be created before running
- Always activate `.venv` before starting exporter
- Docker required for Grafana

---

# Quick Start

### 1. Install Prometheus
### 2. Create venv
```
python3 -m venv .venv
```

### 3. Activate venv
```
source .venv/bin/activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Run system
```
./start.sh
```

---

# Architecture

Linux Processes
   ↓
Python Exporter
   ↓
Prometheus
   ↓
Grafana Dashboard

---