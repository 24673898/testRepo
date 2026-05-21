import re

_DOMAIN_REGEX = re.compile(
    r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$'
)

def _sanitize_domain(value: str) -> str:
    value = re.sub(r'^https?://', '', value, flags=re.IGNORECASE)
    value = value.split('/')[0]
    value = value.split(':')[0]
    value = re.sub(r'<[^>]*>', '', value)
    return value.strip().lower()

def validate_domain(domain: str) -> str:
    cleaned = _sanitize_domain(domain)
    if not cleaned:
        raise ValueError("Domain cannot be empty")
    if re.search(r'[<>"\';&]', cleaned):
        raise ValueError("Domain contains invalid characters")
    if len(cleaned) > 253:
        raise ValueError("Domain name is too long")
    if not _DOMAIN_REGEX.match(cleaned):
        raise ValueError("Invalid domain format — use example.com")
    return cleaned