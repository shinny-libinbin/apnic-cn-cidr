#!/usr/bin/env python3
"""
Fetch CN mainland IP CIDR blocks from APNIC for policy routing.
"""

import ipaddress
import math

import requests

APNIC_URL = "https://ftp.apnic.net/stats/apnic/delegated-apnic-latest"
HTTP_TIMEOUT = 30

# 在这里维护你人工确认属于 CN 的网段, 会并入 APNIC 的 CN 结果.
# 人工确认参照的是 bgp.he.net 公布的自治域内的 CIDR(通过明确知道某个 ip 属于 CN, 反查它的自治域, 该自治域下的 CIDR 都属于 CN 网段).
# 支持 IPv4/IPv6 CIDR, 例如 "1.2.3.0/24" 或 "2408:xxxx::/32".
CUSTOM_CN_CIDRS = [
    "8.133.0.0/16",
]


def fetch_apnic_data():
    """Download APNIC delegated data."""
    print(f"Fetching data from {APNIC_URL} ...")
    resp = requests.get(APNIC_URL, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.text.splitlines()


def parse_cn_ip(lines):
    """Parse CN IPv4 and IPv6 CIDR blocks from APNIC data."""
    ipv4_list = []
    ipv6_list = []

    for line in lines:
        # Skip comments and headers.
        if line.startswith("#") or line.startswith("*") or "|" not in line:
            continue

        fields = line.split("|")
        if len(fields) < 7:
            continue

        _registry, cc, ip_type, start, value = fields[0], fields[1], fields[2], fields[3], fields[4]

        if cc != "CN":
            continue

        if ip_type == "ipv4":
            # APNIC 的 value 是地址数量, 这里换算成 CIDR 前缀长度.
            host_count = int(value)
            prefix_len = 32 - int(math.log2(host_count))
            ipv4_list.append(f"{start}/{prefix_len}")

        elif ip_type == "ipv6":
            # APNIC 的 value 对 IPv6 直接就是前缀长度.
            ipv6_list.append(f"{start}/{value}")

    return collapse_cidrs(ipv4_list), collapse_cidrs(ipv6_list)


def collapse_cidrs(cidr_list):
    """Collapse CIDRs by removing covered subnets and merging adjacent ranges."""
    networks = [ipaddress.ip_network(cidr, strict=False) for cidr in cidr_list]
    return [str(net) for net in ipaddress.collapse_addresses(networks)]


def split_custom_cidrs(cidr_list):
    """Split custom CIDRs into IPv4 and IPv6 lists."""
    custom_ipv4 = []
    custom_ipv6 = []

    for cidr in cidr_list:
        cidr_value = cidr.strip()
        if not cidr_value:
            continue
        try:
            network = ipaddress.ip_network(cidr_value, strict=False)
        except ValueError as exc:
            # 自定义网段来自手工维护时可能出现格式错误, 这里仅告警并跳过.
            print(f"[WARN] Invalid custom CIDR skipped: {cidr_value} ({exc})")
            continue

        if network.version == 4:
            custom_ipv4.append(str(network))
        else:
            custom_ipv6.append(str(network))

    return collapse_cidrs(custom_ipv4), collapse_cidrs(custom_ipv6)


def write_list(filename, ip_list):
    """Write IP list to file."""
    with open(filename, "w") as f:
        f.write("\n".join(ip_list) + "\n")
    print(f"Written {len(ip_list)} entries to {filename}")


def main():
    lines = fetch_apnic_data()
    apnic_ipv4, apnic_ipv6 = parse_cn_ip(lines)
    custom_ipv4, custom_ipv6 = split_custom_cidrs(CUSTOM_CN_CIDRS)

    final_ipv4 = collapse_cidrs(apnic_ipv4 + custom_ipv4)
    final_ipv6 = collapse_cidrs(apnic_ipv6 + custom_ipv6)

    print(
        "Stats: "
        f"APNIC IPv4={len(apnic_ipv4)}, APNIC IPv6={len(apnic_ipv6)}, "
        f"Custom IPv4={len(custom_ipv4)}, Custom IPv6={len(custom_ipv6)}, "
        f"Final IPv4={len(final_ipv4)}, Final IPv6={len(final_ipv6)}"
    )

    write_list("cn_ipv4.txt", final_ipv4)
    write_list("cn_ipv6.txt", final_ipv6)
    print("Done.")


if __name__ == "__main__":
    main()
