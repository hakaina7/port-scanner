import argparse
import time
from scanner import run_scan
from utils import parse_ports


def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner")

    parser.add_argument("--host", required=True, help="Target host")
    parser.add_argument("--ports", default="1-1024", help="Port range (e.g. 20-80)")
    parser.add_argument("--timeout", type=float, default=1, help="Timeout per port")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--save", action="store_true", help="Save results to file")

    args = parser.parse_args()

    ports = parse_ports(args.ports)

    print(f"\nScanning {args.host}...\n")

    start_time = time.time()
    open_ports = run_scan(args.host, ports, args.timeout, args.threads)
    scan_time = round(time.time() - start_time, 2)

    if open_ports:
        print("Open ports:")
        for port, banner in sorted(open_ports.items()):
            print(f"Port {port} — OPEN")
            if banner:
                print(f"  Banner: {banner}")
    else:
        print("No open ports found.")

    print(f"\nScan completed in {scan_time} seconds")

    if args.save:
        with open("scan_report.txt", "w") as f:
            for port, banner in open_ports.items():
                f.write(f"Port {port} — OPEN\n")
                f.write(f"Banner: {banner}\n\n")

        print("Report saved to scan_report.txt")


if __name__ == "__main__":
    main()
