import typer
import yaml
import sys
import logging
import json
from pathlib import Path
from devops_toolkit.services.dns_service import check_domains, logger

app = typer.Typer(help="Narzędzie do monitorowania certyfikatów SSL/DNS.")


@app.command()
def check(
    config_path: str = typer.Option(
        "config/example.yaml", "--config", "-c", help="Ścieżka do pliku konfiguracyjnego"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Włącz tryb DEBUG"),
    json_output: bool = typer.Option(False, "--json", help="Zwróć wynik w formacie JSON"),
):
    """
    Sprawdza certyfikaty SSL dla domen zdefiniowanych w pliku YAML.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    config_file = Path(config_path)
    if not config_file.exists():
        typer.secho(
            f"Błąd: Nie znaleziono pliku konfiguracyjnego: {config_path}", fg=typer.colors.RED
        )
        raise typer.Exit(code=2)

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    dns_config = config.get("dns_monitor", {})
    domains = dns_config.get("domains", [])
    warn_days = dns_config.get("warn_days", 14)

    if not domains:
        typer.secho("Błąd: Brak zdefiniowanych domen w pliku YAML.", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    logger.debug(
        f"Wczytano {len(domains)} domen do sprawdzenia. Próg ostrzegawczy: {warn_days} dni."
    )

    has_errors, results = check_domains(domains, warn_days)

    if json_output:
        typer.echo(
            json.dumps(
                {
                    "domains_checked": len(domains),
                    "warn_days": warn_days,
                    "has_errors": has_errors,
                    "results": results,
                }
            )
        )
        sys.exit(1 if has_errors else 0)

    if has_errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    app()
