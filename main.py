import argparse
import os
import time
import json
import logging
from datetime import datetime
from colorama import Fore, init
from tqdm import tqdm
from scanner import run_scan
from utils import parse_ports

init(autoreset=True)
logging.basicConfig(filename="scan.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("--host", required=True, help="Target host")
    parser.add_argument("--ports", default="1-1024", help="Port range (e.g. 20-80)")
    parser.add_argument("--timeout", type=float, default=1, help="Timeout per port")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--protocol", choices=["tcp", "udp"], default="tcp", help="Protocol to scan")
    parser.add_argument("--save", action="store_true", help="Save results to TXT")
    parser.add_argument("--json", action="store_true", help="Save results to JSON")

    args = parser.parse_args()
    ports = list(parse_ports(args.ports))

    print(f"\nScanning {args.host} ({args.protocol.upper()})...\n")
    start_time = time.time()

    scan_results = run_scan(args.host, ports, args.timeout, args.threads, protocol=args.protocol)

    # Собираем открытые порты
    open_ports = {port: banner for port, banner in scan_results if banner is not None}

    scan_time = round(time.time() - start_time, 2)

    # Цветной вывод
    if open_ports:
        print(Fore.GREEN + "Open ports:")
        for port, banner in sorted(open_ports.items()):
            print(Fore.GREEN + f"Port {port} — OPEN")
            if banner:
                print(Fore.YELLOW + f"  Banner: {banner}")
                logging.info(f"{args.protocol.upper()} Port {port} OPEN: {banner}")
    else:
        print(Fore.RED + "No open ports found.")

    # Простая детекция firewall/rate-limit
    total_ports = len(ports)
    filtered_ports = sum(1 for _, banner in scan_results if banner is None)
    if filtered_ports / total_ports > 0.5:
        print(Fore.MAGENTA + "Warning: more than 50% ports are filtered/closed. Possible firewall or rate-limiting detected.")

    print(f"\nScan completed in {scan_time} seconds")

    # Создаём папку reports
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # TXT отчет
    if args.save:
        txt_path = os.path.join("reports", f"scan_report_{timestamp}.txt")
        with open(txt_path, "w") as f:
            for port, banner in open_ports.items():
                f.write(f"{args.protocol.upper()} Port {port} — OPEN\n")
                f.write(f"Banner: {banner}\n\n")
        print(Fore.CYAN + f"Report saved to {txt_path}")

    # JSON отчет
    if args.json:
        json_path = os.path.join("reports", f"scan_report_{timestamp}.json")
        with open(json_path, "w") as f:
            json.dump({
                "host": args.host,
                "protocol": args.protocol.upper(),
                "scan_time": scan_time,
                "open_ports": open_ports
            }, f, indent=4)
        print(Fore.CYAN + f"Report saved to {json_path}")

if __name__ == "__main__":
    main()