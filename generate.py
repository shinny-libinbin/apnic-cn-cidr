#!/usr/bin/env python3
"""
Fetch CN mainland IP CIDR blocks from APNIC for policy routing.
"""

import math
import requests

APNIC_URL = "https://ftp.apnic.net/stats/apnic/delegated-apnic-latest"


def fetch_apnic_data():
    """Download APNIC delegated data."""
    print(f"Fetching data from {APNIC_URL} ...")
    resp = requests.get(APNIC_URL, timeout=30)
    resp.raise_for_status()
    return resp.text.splitlines()


def parse_cn_ip(lines):
    """Parse CN IPv4 and IPv6 CIDR blocks from APNIC data."""
    ipv4_list = []
    ipv6_list = []

    for line in lines:
        # skip comments and headers
        if line.startswith("#") or line.startswith("*") or "|" not in line:
            continue

        fields = line.split("|")
        if len(fields) < 7:
            continue

        registry, cc, ip_type, start, value = fields[0], fields[1], fields[2], fields[3], fields[4]

        if cc != "CN":
            continue

        if ip_type == "ipv4":
            # value = host count, convert to CIDR prefix
            host_count = int(value)
            prefix_len = 32 - int(math.log2(host_count))
            ipv4_list.append(f"{start}/{prefix_len}")

        elif ip_type == "ipv6":
            # value = prefix length
            ipv6_list.append(f"{start}/{value}")

    return ipv4_list, ipv6_list


def write_list(filename, ip_list):
    """Write IP list to file."""
    with open(filename, "w") as f:
        f.write("\n".join(ip_list) + "\n")
    print(f"Written {len(ip_list)} entries to {filename}")


def main():
    lines = fetch_apnic_data()
    ipv4_list, ipv6_list = parse_cn_ip(lines)
    write_list("cn_ipv4.txt", ipv4_list)
    write_list("cn_ipv6.txt", ipv6_list)
    print("Done.")


if __name__ == "__main__":
    main()