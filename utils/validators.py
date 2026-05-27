import re
import ipaddress
from typing import Optional

def validate_domain(domain: str) -> Optional[str]:
    """
    Sanitizes and validates a domain name string according to RFC 1035 spec.
    
    Ensures the domain is lowercase, does not exceed 253 characters, and
    each label is between 1 and 63 characters consisting of alphanumeric 
    characters or hyphens, and does not start or end with a hyphen.

    Args:
        domain: The raw domain string to validate.

    Returns:
        The sanitized, lowercase domain string if valid, or None if invalid.
    """
    if not domain:
        return None
        
    sanitized = domain.strip().lower()
    
    if sanitized.endswith('.'):
        sanitized = sanitized[:-1]
        
    if len(sanitized) < 1 or len(sanitized) > 253:
        return None
        
    domain_regex = re.compile(
        r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$',
        re.IGNORECASE
    )
    
    if not domain_regex.match(sanitized):
        return None
        
    return sanitized

def validate_ip_address(ip_str: str) -> Optional[str]:
    """
    Validates that a string represents a valid IPv4 or IPv6 address.
    
    Utilizes Python's built-in ipaddress module to perform strict structural
    validation on the provided input string.

    Args:
        ip_str: The raw IP address string to validate.

    Returns:
        The standardized, stripped IP address string if valid, or None if invalid.
    """
    if not ip_str:
        return None
        
    sanitized = ip_str.strip()
    
    try:
        ip_obj = ipaddress.ip_address(sanitized)
        return str(ip_obj)
    except ValueError:
        return None