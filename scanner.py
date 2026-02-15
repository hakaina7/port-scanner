import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# ------------------ TCP ------------------
def scan_tcp_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                banner = grab_banner_tcp(s)
                return port, banner
    except Exception:
        pass
    return None

def grab_banner_tcp(sock):
    try:
        sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner[:100] if banner else "No banner"
    except Exception:
        return "No banner"

# ------------------ UDP ------------------
def scan_udp_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(b"\x00", (host, port))
            s.recvfrom(1024)
            return port, "UDP open"
    except socket.timeout:
        return port, "UDP open/filtered"
    except ConnectionRefusedError:
        return port, None
    except Exception:
        return port, None

# ------------------ Run scan ------------------
def run_scan(host, ports, timeout=1, threads=100, protocol="tcp"):
    results = []
    scan_func = scan_tcp_port if protocol.lower() == "tcp" else scan_udp_port

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_func, host, port, timeout): port for port in ports}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
            else:
                results.append((futures[future], None))
    return results