import json
from typing import Dict, List, Any

class ResultFormatter:
    """
    Formats discovered DNS architecture data into structured JSON, text summaries, 
    or clean ASCII terminal tables for reporting.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initializes the formatter with raw DNS data containing standard records, 
        brute-forced subdomains, and zone transfer status.
        """
        self.data: Dict[str, Any] = data

    def to_json(self) -> str:
        """
        Serializes the structured DNS architecture data into a pretty-printed JSON string.
        """
        return json.dumps(self.data, indent=4)

    def to_text_summary(self) -> str:
        """
        Generates a structured plain-text summary highlighting key findings 
        such as the target domain, discovered record counts, and zone transfer vulnerabilities.
        """
        target: str = self.data.get("target", "Unknown Target")
        records: Dict[str, List[str]] = self.data.get("records", {})
        subdomains: List[Dict[str, Any]] = self.data.get("subdomains", [])
        zone_transfer: Dict[str, Any] = self.data.get("zone_transfer", {})

        summary: List[str] = [
            f"DNS ENUMERATION REPORT FOR: {target}",
            "=" * 50,
            f"Standard Records Found: {sum(len(v) for v in records.values())}",
            f"Subdomains Discovered:  {len(subdomains)}",
            f"Zone Transfer Status:   {'VULNERABLE' if zone_transfer.get('vulnerable') else 'SECURE'}",
            ""
        ]

        if records:
            summary.append("--- Standard Records ---")
            for record_type, values in records.items():
                if values:
                    summary.append(f"[{record_type}]")
                    for val in values:
                        summary.append(f"  - {val}")
            summary.append("")

        if subdomains:
            summary.append("--- Discovered Subdomains ---")
            for sub in subdomains:
                name: str = sub.get("subdomain", "")
                ips: str = ", ".join(sub.get("ips", []))
                summary.append(f"  - {name} -> [{ips}]")
            summary.append("")

        if zone_transfer.get("vulnerable") and zone_transfer.get("records"):
            summary.append("--- Leaked Zone Transfer Records ---")
            for leaked in zone_transfer.get("records", []):
                summary.append(f"  - {leaked}")
            summary.append("")

        return "\n".join(summary)

    def to_terminal_table(self) -> str:
        """
        Constructs visual ASCII terminal tables separating standard infrastructure records 
        from brute-forced subdomains for high-readability command-line display.
        """
        output: List[str] = []
        
        records: Dict[str, List[str]] = self.data.get("records", {})
        if records and any(records.values()):
            output.append("=== STANDARD DNS RECORDS ===")
            output.append(f"{'TYPE':<8} | {'RECORD DATA'}")
            output.append("-" * 50)
            for r_type, r_values in records.items():
                for val in r_values:
                    output.append(f"{r_type:<8} | {val}")
            output.append("")

        subdomains: List[Dict[str, Any]] = self.data.get("subdomains", [])
        if subdomains:
            output.append("=== DISCOVERED SUBDOMAINS ===")
            output.append(f"{'SUBDOMAIN':<30} | {'RESOLVED IPS'}")
            output.append("-" * 50)
            for sub in subdomains:
                name: str = sub.get("subdomain", "")
                ips: str = ", ".join(sub.get("ips", []))
                output.append(f"{name:<30} | {ips}")
            output.append("")

        zone_transfer: Dict[str, Any] = self.data.get("zone_transfer", {})
        if zone_transfer:
            output.append("=== ZONE TRANSFER STATUS ===")
            vuln_status: str = "VULNERABLE (AXFR SUCCESSFUL)" if zone_transfer.get("vulnerable") else "SECURE (AXFR REFUSED)"
            output.append(f"Status: {vuln_status}")
            output.append("")

        return "\n".join(output)