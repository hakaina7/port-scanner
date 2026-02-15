import argparse
import time
from scanner import scan_ports
from utils import validate_host, parse_ports
from report import save_txt_report, save_pdf_report
from colorama import Fore, init
from report import save_txt_report, save_pdf_report

init(autoreset=True)


def print_colored_results(results):
    for port, status in results:
        if status == "open":
            print(Fore.GREEN + f"{port}: {status}")
        elif status == "closed":
            print(Fore.RED + f"{port}: {status}")
        else:
            print(Fore.YELLOW + f"{port}: {status}")


def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("--host", type=str, required=True, help="Target IP or hostname")
    parser.add_argument("--ports", type=str, default="1-1024", help="Ports (20-80 or 22,80,443)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout per port (seconds)")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads")
    parser.add_argument("--save", action="store_true", help="Save report as TXT")
    parser.add_argument("--pdf", action="store_true", help="Save report as PDF")

    args = parser.parse_args()

    if not validate_host(args.host):
        print(Fore.RED + "Invalid host or IP address.")
        return

    ports = parse_ports(args.ports)

    print(Fore.CYAN + f"Scanning {args.host} ports: {args.ports} with {args.threads} threads...\n")

    start_time = time.time()
    results = scan_ports(args.host, ports, args.timeout, args.threads)
    scan_time = round(time.time() - start_time, 2)

    print_colored_results(results)

    print(Fore.CYAN + f"\nScan completed in {scan_time} seconds")

    if args.save:
        txt_file = save_txt_report(args.host, results)
        print(Fore.CYAN + f"TXT report saved to {txt_file}")

    if args.pdf:
        pdf_file = save_pdf_report(args.host, results, scan_time)
        print(Fore.CYAN + f"PDF report saved to {pdf_file}")


if __name__ == "__main__":
    main()
