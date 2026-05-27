import logging
from typing import Dict, Any, Optional
from utils.validators import validate_domain, validate_ip_address
from core.resolver import DNSQueryEngine
from core.bruteforcer import SubdomainBruteforcer
from output.reporter import ResultFormatter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DNSEnumOrchestrator")

class DNSEnumOrchestrator:
    """
    Coordinates the DNS enumeration workflow by validating inputs,
    performing standard record resolution, executing subdomain brute-forcing,
    and structuring the collected data for reporting.
    """
    def __init__(self, target_domain: str, wordlist_path: Optional[str] = None, nameserver: Optional[str] = None) -> None:
        """
        Initializes the orchestrator with target details and configurations.
        """
        self.target_domain = target_domain.strip()
        self.wordlist_path = wordlist_path
        self.nameserver = nameserver.strip() if nameserver else None
        self.results: Dict[str, Any] = {
            "target": self.target_domain,
            "records": {},
            "subdomains": []
        }

    def run(self) -> Dict[str, Any]:
        """
        Executes the full enumeration pipeline sequentially.
        Validates inputs, resolves standard records, and performs brute-forcing if a wordlist is given.
        """
        logger.info(f"Starting DNS enumeration orchestration for: {self.target_domain}")
        
        if not validate_domain(self.target_domain):
            logger.error(f"Invalid target domain provided: {self.target_domain}")
            return {"error": "Invalid target domain"}

        if self.nameserver and not validate_ip_address(self.nameserver):
            logger.error(f"Invalid nameserver IP provided: {self.nameserver}")
            return {"error": "Invalid nameserver IP"}

        try:
            resolver = DNSQueryEngine(nameserver=self.nameserver)
            logger.info("Querying standard DNS records...")
            self.results["records"] = resolver.resolve_all(self.target_domain)
        except Exception as e:
            logger.error(f"Standard resolution encountered an error: {str(e)}")

        if self.wordlist_path:
            try:
                logger.info(f"Beginning subdomain brute-forcing using: {self.wordlist_path}")
                bruteforcer = SubdomainBruteforcer(
                    domain=self.target_domain,
                    wordlist_path=self.wordlist_path,
                    nameserver=self.nameserver
                )
                self.results["subdomains"] = bruteforcer.execute()
                logger.info(f"Brute-forcing complete. Discovered {len(self.results['subdomains'])} subdomains.")
            except Exception as e:
                logger.error(f"Subdomain brute-forcing encountered an error: {str(e)}")
        else:
            logger.info("No wordlist provided. Skipping subdomain brute-forcing phase.")

        return self.results

    def generate_report(self, format_type: str = "text") -> str:
        """
        Formats the collected orchestration results into the specified format type using the ResultFormatter.
        """
        formatter = ResultFormatter(self.results)
        if format_type.lower() == "json":
            return formatter.to_json()
        elif format_type.lower() == "csv":
            return formatter.to_csv()
        return formatter.to_text_table()