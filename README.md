# apnic-cn-list

Fetch CN mainland IP CIDR blocks from [APNIC](https://ftp.apnic.net/stats/apnic/delegated-apnic-latest) for policy routing.

## Data Source

- APNIC: https://ftp.apnic.net/stats/apnic/delegated-apnic-latest

## Custom CN CIDR Merge

If you have CIDRs that are confirmed CN but not marked as `CN` in APNIC, add them to `CUSTOM_CN_CIDRS` in `generate.py`.

- Supports IPv4 and IPv6 CIDR strings
- The script merges custom CIDRs with APNIC CN results
- Final output is collapsed to remove overlaps and adjacent ranges

## Files

| File | Description |
|------|-------------|
| `cn_ipv4.txt` | CN mainland IPv4 CIDR list |
| `cn_ipv6.txt` | CN mainland IPv6 CIDR list |

## Use Cases

- Policy routing
- Traffic splitting
- IP whitelist / blacklist

## Update Frequency

Automatically updated daily via GitHub Actions.

## License

Data copyright belongs to [APNIC](https://www.apnic.net/). This repository only provides formatted aggregation.