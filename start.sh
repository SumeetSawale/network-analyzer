#!/bin/bash

echo "Starting Grafana..."
docker-compose up -d

echo "Starting Prometheus..."

# Find Prometheus folder automatically
PROM_DIR=$(find . -maxdepth 1 -type d -name "prometheus*" | head -n 1)

if [ -z "$PROM_DIR" ]; then
  echo "ERROR: Prometheus directory not found!"
  exit 1
fi

echo "Using Prometheus directory: $PROM_DIR"

# Start Prometheus from inside folder
$PROM_DIR/prometheus --config.file=$PWD/prometheus.yml &

echo "Starting Exporter..."

# Activate virtual environment
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

python3 app_net_exporter.py &

echo "System ready"
echo "Grafana: http://localhost:3000"
echo "Prometheus: http://localhost:9090"
