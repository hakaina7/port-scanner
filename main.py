import argparse
import time
import json
import logging
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
    parser.add_argument("--save", action="store_true", help="Save results to TXT")
    parser.add_argument("--json", action="store_true", help="Save results to JSON")

    args = parser.parse_args()
    ports = list(parse_ports(args.ports))

    print(f"\nScanning {args.host}...\n")
    start_time = time.time()

    # Запуск сканирования
    scan_results = run_scan(args.host, ports, args.timeout, args.threads)

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
                logging.info(f"Port {port} OPEN: {banner}")
    else:
        print(Fore.RED + "No open ports found.")

    print(f"\nScan completed in {scan_time} seconds")

    # TXT отчет
    if args.save:
        with open("scan_report.txt", "w") as f:
            for port, banner in open_ports.items():
                f.write(f"Port {port} — OPEN\n")
                f.write(f"Banner: {banner}\n\n")
        print(Fore.CYAN + "Report saved to scan_report.txt")

    # JSON отчет
    if args.json:
        with open("scan_report.json", "w") as f:
            json.dump({"host": args.host, "scan_time": scan_time, "open_ports": open_ports}, f, indent=4)
        print(Fore.CYAN + "Report saved to scan_report.json")

if __name__ == "__main__":
    main()