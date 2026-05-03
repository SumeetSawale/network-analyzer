from prometheus_client import start_http_server, Gauge
import psutil
import time
import subprocess
import re
import socket

# Metrics
rx_g = Gauge('app_rx_bytes', 'RX bytes per app', ['pid', 'app'])
tx_g = Gauge('app_tx_bytes', 'TX bytes per app', ['pid', 'app'])
conn_g = Gauge('app_connections', 'Active connections', ['pid', 'app', 'dst', 'host'])
dns_g = Gauge('app_dns_info', 'DNS mapping', ['pid', 'app', 'ip', 'host'])

# Simple DNS cache (to avoid repeated lookups)
dns_cache = {}

def reverse_dns(ip):
    if ip in dns_cache:
        return dns_cache[ip]

    try:
        host = socket.gethostbyaddr(ip)[0]
    except:
        host = "unknown"

    dns_cache[ip] = host
    return host


def get_connections():
    try:
        result = subprocess.check_output("ss -tunp", shell=True).decode()
    except:
        return []

    lines = result.split("\n")
    data = []

    for line in lines:
        if "pid=" in line:
            try:
                pid = re.search(r'pid=(\d+)', line).group(1)
                app = re.search(r'"(.*?)"', line).group(1)
                dst = line.split()[-2]

                # Extract IP (remove port)
                if dst.startswith('['):  
                    continue  # skip IPv6 or malformed

                ip = dst.rsplit(':', 1)[0]
                data.append((pid, app, dst, ip))
            except:
                continue

    return data


def collect():
    conns = get_connections()

    for pid, app, dst, ip in conns:
        try:
            p = psutil.Process(int(pid))
            io = p.io_counters()

            # RX / TX
            rx_g.labels(pid=pid, app=app).set(io.read_bytes)
            tx_g.labels(pid=pid, app=app).set(io.write_bytes)

            # Connection
            host = reverse_dns(ip)
            conn_g.labels(pid=pid, app=app, dst=dst, host=host).set(1)
            
            # Reverse DNS
            host = reverse_dns(ip)
            dns_g.labels(pid=pid, app=app, ip=ip, host=host).set(1)

        except:
            continue


if __name__ == "__main__":
    print("Exporter running at http://localhost:8000/metrics")
    start_http_server(8000)

    while True:
        collect()
        time.sleep(1)
