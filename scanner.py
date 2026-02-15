import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# ------------------ Сканирование ------------------
def scan_port(host, port, timeout):
    """Сканирует один TCP порт и пытается получить баннер."""
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
    """Пробуем прочитать баннер сервиса (HTTP HEAD запрос)."""
    try:
        sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner[:100] if banner else "No banner"
    except Exception:
        return "No banner"

# ------------------ Запуск сканирования ------------------
def run_scan(host, ports, timeout=1, threads=100):
    """Сканируем список портов с многопоточностью."""
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, host, port, timeout): port for port in ports}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
            else:
                results.append((futures[future], None))  # для прогресс-бара
    return results
