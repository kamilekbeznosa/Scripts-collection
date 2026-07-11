import time
import logging
import requests
from typing import List, Dict, Tuple
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _make_github_request(url: str, token: str) -> requests.Response:
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code in (403, 429) and "X-RateLimit-Remaining" in response.headers:
        if response.headers["X-RateLimit-Remaining"] == "0":
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            sleep_time = max(reset_time - time.time(), 0) + 1
            logger.warning(
                f"Osiągnięto limit API GitHuba! Wstrzymuję działanie na {sleep_time} sekund..."
            )
            time.sleep(sleep_time)
            return _make_github_request(url, token)

    response.raise_for_status()
    return response


def get_all_repositories(target: str, token: str, is_org: bool = False) -> List[Dict]:
    """Pobiera wszystkie repozytoria, obsługując paginację (kolejne strony wyników)."""
    repos = []
    base_url = (
        f"https://api.github.com/orgs/{target}/repos"
        if is_org
        else f"https://api.github.com/users/{target}/repos"
    )
    url = f"{base_url}?per_page=100"

    while url:
        logger.debug(f"Pobieranie strony API: {url}")
        response = _make_github_request(url, token)
        repos.extend(response.json())

        url = response.links.get("next", {}).get("url")

    return repos


def audit_target(target: str, token: str, is_org: bool) -> Tuple[bool, List[str]]:
    has_errors = False
    results = []

    try:
        repos = get_all_repositories(target, token, is_org)
        logger.info(f"Pobrano {len(repos)} repozytoriów dla '{target}'. Rozpoczynam audyt...")

        for repo in repos:
            name = repo["name"]
            issues = []

            if not repo.get("description"):
                issues.append("Brak opisu (description)")

            if not repo.get("has_issues"):
                issues.append("Wyłączone Issues (śledzenie błędów)")

            if issues:
                msg = f"[FAIL] {name}: {', '.join(issues)}"
                logger.warning(msg)
                results.append(msg)
                has_errors = True
            else:
                msg = f"[PASS] {name} - Zgodne z polityką"
                logger.info(msg)
                results.append(msg)

    except requests.exceptions.RequestException as e:
        logger.error(f"Krytyczny błąd połączenia z GitHub API: {e}")
        has_errors = True

    return has_errors, results
