import ssl
import socket
import logging
from datetime import datetime, timezone
from typing import List, Tuple

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_cert_expiry_date(domain: str) -> datetime:
    """Pobiera datę wygaśnięcia certyfikatu SSL dla domeny."""
    context = ssl.create_default_context()

    with socket.create_connection((domain, 443), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

            if not cert:
                raise ValueError("Brak certyfikatu")

            expire_str = cert["notAfter"]
            return datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z").replace(
                tzinfo=timezone.utc
            )


def check_domains(domains: List[str], warn_days: int) -> Tuple[bool, List[str]]:
    """
    Sprawdza listę domen. Zwraca flagę has_errors oraz listę wyników.
    """
    has_errors = False
    results = []

    now = datetime.now(timezone.utc)

    for domain in domains:
        try:
            logger.debug(f"Sprawdzanie certyfikatu dla: {domain}")
            expiry_date = get_cert_expiry_date(domain)
            days_left = (expiry_date - now).days

            if days_left <= warn_days:
                msg = f"[WARNING] {domain} wygasa za {days_left} dni! ({expiry_date.date()})"
                logger.warning(msg)
                results.append(msg)
                has_errors = True
            else:
                msg = f"[OK] {domain} ma ważny certyfikat (pozostało dni: {days_left})"
                logger.info(msg)
                results.append(msg)

        except Exception as e:
            msg = f"[ERROR] Nie można sprawdzić {domain}: {str(e)}"
            logger.error(msg)
            results.append(msg)
            has_errors = True

    return has_errors, results
