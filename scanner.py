import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                banner = grab_banner(s)
                return port, banner
    except Exception:
        pass
    return None


def grab_banner(sock):
    try:
        sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner[:100] if banner else "No banner"
    except Exception:
        return "No banner"


def run_scan(host, ports, timeout=1, threads=100):
    open_ports = {}

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, host, port, timeout): port
            for port in ports
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                port, banner = result
                open_ports[port] = banner

    return open_ports