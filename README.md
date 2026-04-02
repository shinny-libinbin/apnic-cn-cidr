# apnic-cn-list

Fetch CN mainland IP CIDR blocks from [APNIC](https://ftp.apnic.net/stats/apnic/delegated-apnic-latest) for policy routing.

## Data Source

- APNIC: https://ftp.apnic.net/stats/apnic/delegated-apnic-latest

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