import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(host, port, timeout):
    """Сканирует один порт"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            result = s.connect_ex((host, port))
            if result == 0:
                return (port, "open")
            else:
                return (port, "closed")
        except socket.timeout:
            return (port, "filtered")
        except Exception:
            return (port, "error")

def scan_ports(host, ports, timeout=1.0, threads=50):
    """Многопоточное сканирование портов"""
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_port = {executor.submit(scan_port, host, port, timeout): port for port in ports}
        for future in as_completed(future_to_port):
            results.append(future.result())
    return sorted(results, key=lambda x: x[0])
