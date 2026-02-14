import re
import socket

def validate_host(host):
    """Проверяет корректность IP или домена"""
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(ip_pattern, host):
        return True
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False

def parse_ports(ports_str):
    """Парсит диапазон или список портов"""
    ports = set()
    for part in ports_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.update(range(int(start), int(end)+1))
        else:
            ports.add(int(part))
    return sorted(list(ports))
