# DNS Enumeration Tool
> High-performance DNS reconnaissance and subdomain discovery framework for Red Team operations.

## Description
The **DNS Enumeration Tool** is a professional, modular Python 3 framework designed for network reconnaissance and target surface mapping. It automates the discovery of critical DNS architecture by combining passive record retrieval, aggressive dictionary-based subdomain brute-forcing, and low-level nameserver queries. 

Built with scalability in mind, the tool handles large-scale wordlist streaming and supports direct AXFR zone transfers to uncover hidden internal infrastructure.

## File Structure
```text
├── main.py                # CLI entrypoint; parses arguments and invokes orchestrator
├── core/
│   ├── orchestrator.py    # Coordinates validation, resolution, brute-forcing, and reporting
│   ├── resolver.py        # Queries standard records (A, AAAA, MX, TXT, NS, SOA)
│   └── bruteforcer.py     # Executes dictionary-based subdomain discovery
├── network/
│   └── dns_client.py      # Manages UDP/TCP sockets and processes AXFR zone transfers
├── output/
│   └── reporter.py        # Formats architecture into tables, JSON payloads, or text
└── utils/
    ├── cli_parser.py      # Defines CLI flags, options, and help menus
    ├── io_helpers.py      # Handles reliable, chunked streaming of large wordlists
    └── validators.py      # Sanitizes domain names, IPs, and custom nameservers
```

## Requirements
* Python 3.8+
* `dnspython` (for advanced record resolution)
* `tabulate` (for clean terminal tables)

## Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/yourusername/dns-enumeration-tool.git
cd dns-enumeration-tool
pip install -r requirements.txt
```

## Usage
Run the tool via the CLI entrypoint to view all available flags and options:

```bash
python3 main.py --help
```

### Standard Enumeration
```bash
python3 main.py -d target.com
```

### Subdomain Brute-Forcing with Zone Transfer
```bash
python3 main.py -d target.com -w wordlists/subdomains.txt --axfr --output json
```

## Disclaimer
> **Notice:** This tool is intended strictly for authorized penetration testing, authorized red teaming, and educational security assessments. Unauthorized scanning of infrastructure without explicit, prior written consent is illegal.