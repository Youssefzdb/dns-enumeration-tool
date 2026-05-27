import argparse
from typing import List, Optional

def parse_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parses command-line arguments for the DNS Enumeration Tool.

    This function configures the argument parser with options for targeted 
    domain specification, custom nameservers, wordlist paths for subdomain 
    brute-forcing, output formatting, and zone transfer attempts.

    Args:
        args: Optional list of command-line arguments to parse. 
              Defaults to sys.argv[1:] if None.

    Returns:
        argparse.Namespace: An object containing the parsed command-line flags.
    """
    parser = argparse.ArgumentParser(
        description="DNS Enumeration and Subdomain Discovery Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-d", "--domain",
        required=True,
        type=str,
        help="Target domain to enumerate (e.g., example.com)"
    )

    parser.add_argument(
        "-n", "--nameserver",
        type=str,
        default=None,
        help="Custom DNS server IP address to query (e.g., 8.8.8.8)"
    )

    parser.add_argument(
        "-w", "--wordlist",
        type=str,
        default=None,
        help="Path to a text file containing subdomains for brute-forcing"
    )

    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=10,
        help="Number of concurrent threads to use during brute-forcing"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Path to write the enumeration results file"
    )

    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Format for the output report"
    )

    parser.add_argument(
        "-x", "--axfr",
        action="store_true",
        help="Attempt an asynchronous zone transfer (AXFR) against target nameservers"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output logging"
    )

    return parser.parse_args(args)