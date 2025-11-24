"""vCard generation utility for RFC 3.0 compliant contact format."""
from typing import Optional, Dict


def escape_vcard_value(value: str) -> str:
    """Escape special characters for vCard format."""
    if not value:
        return ""
    # Replace commas, semicolons, and newlines
    value = value.replace("\\", "\\\\")
    value = value.replace(",", "\\,")
    value = value.replace(";", "\\;")
    value = value.replace("\n", "\\n")
    return value


def generate_vcard(
    full_name: str,
    job_title: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    whatsapp: Optional[str] = None,
    company_name: Optional[str] = None,
    photo_url: Optional[str] = None,
    bio: Optional[str] = None,
    social_links: Optional[Dict[str, str]] = None,
) -> str:
    """
    Generate RFC 3.0 compliant vCard format.
    
    Args:
        full_name: Employee full name (required)
        job_title: Job title/position
        email: Email address
        phone: Phone number
        whatsapp: WhatsApp number
        company_name: Company name
        photo_url: URL to photo/avatar
        bio: Employee bio/description
        social_links: Dictionary of social links (linkedin, twitter, etc)
    
    Returns:
        RFC 3.0 compliant vCard string
    """
    lines = []
    
    # Begin vCard
    lines.append("BEGIN:VCARD")
    lines.append("VERSION:3.0")
    
    # Format Name (FN) - required
    lines.append(f"FN:{escape_vcard_value(full_name)}")
    
    # Structured Name (N) - required
    # Format: N:LastName;FirstName;;;
    name_parts = full_name.split(" ", 1)
    last_name = escape_vcard_value(name_parts[-1]) if len(name_parts) > 1 else escape_vcard_value(full_name)
    first_name = escape_vcard_value(name_parts[0]) if len(name_parts) > 1 else ""
    lines.append(f"N:{last_name};{first_name};;;")
    
    # Title (TITLE)
    if job_title:
        lines.append(f"TITLE:{escape_vcard_value(job_title)}")
    
    # Organization (ORG)
    if company_name:
        lines.append(f"ORG:{escape_vcard_value(company_name)}")
    
    # Email (EMAIL)
    if email:
        lines.append(f"EMAIL;TYPE=INTERNET:{escape_vcard_value(email)}")
    
    # Telephone (TEL)
    if phone:
        lines.append(f"TEL;TYPE=VOICE:{escape_vcard_value(phone)}")
    
    if whatsapp:
        lines.append(f"TEL;TYPE=CELL:{escape_vcard_value(whatsapp)}")
    
    # Note/Bio (NOTE)
    if bio:
        lines.append(f"NOTE:{escape_vcard_value(bio)}")
    
    # Photo (PHOTO)
    if photo_url:
        lines.append(f"PHOTO;VALUE=URI:{photo_url}")
    
    # URL - for social links
    if social_links:
        if isinstance(social_links, dict):
            for platform, url in social_links.items():
                if url:
                    lines.append(f"URL;TYPE={platform.upper()}:{escape_vcard_value(url)}")
    
    # End vCard
    lines.append("END:VCARD")
    
    return "\n".join(lines)
