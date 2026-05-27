import dns.resolver
from typing import Dict, List, Any
from network.dns_client import RawDNSClient

class DNSQueryEngine:
    """
    Engine to perform standard DNS record queries against a target domain.
    Queries for A, AAAA, MX, TXT, NS, and SOA records using the system resolver
    or a specific nameserver if configured via RawDNSClient integration context.
    """
    
    def __init__(self, nameservers: List[str] = None):
        """
        Initializes the query engine with optional specific nameservers.
        
        :param nameservers: List of IP addresses of nameservers to use for queries.
        """
        self.resolver = dns.resolver.Resolver()
        if nameservers:
            self.resolver.nameservers = nameservers

    def query_record(self, domain: str, record_type: str) -> List[str]:
        """
        Queries a specific DNS record type for a given domain.
        
        :param domain: The target domain name to query.
        :param record_type: The string representation of the record type (e.g., 'A', 'MX').
        :return: A list of string representations of the resolved records.
        """
        results: List[str] = []
        try:
            answers = self.resolver.resolve(domain, record_type)
            for rdata in answers:
                if record_type == 'MX':
                    results.append(f"{rdata.preference} {rdata.exchange.to_text()}")
                elif record_type in ['NS', 'SOA']:
                    results.append(rdata.to_text())
                elif record_type == 'TXT':
                    results.append("".join([b.decode('utf-8', errors='ignore') for b in rdata.strings]))
                else:
                    results.append(rdata.to_text())
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers):
            pass
        return results

    def query_all_standard_records(self, domain: str) -> Dict[str, List[str]]:
        """
        Queries for all standard target records (A, AAAA, MX, TXT, NS, SOA) for a domain.
        
        :param domain: The target domain name to scan.
        :return: A dictionary mapping each record type to its list of resolved strings.
        """
        record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'SOA']
        manifest: Dict[str, List[str]] = {}
        
        for rtype in record_types:
            manifest[rtype] = self.query_record(domain, rtype)
            
        return manifest