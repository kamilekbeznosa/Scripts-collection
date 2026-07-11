import os
import sys
import typer
import logging
import json
from devops_toolkit.services.github_service import audit_target, logger

app = typer.Typer(help="Audytor zgodności repozytoriów na GitHubie.")

@app.command()
def audit(
    target: str = typer.Argument(..., help="Nazwa użytkownika lub organizacji na GitHubie (np. microsoft)"),
    is_org: bool = typer.Option(False, "--org", help="Oznacz, jeśli cel to Organizacja, a nie pojedynczy użytkownik"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Włącz tryb DEBUG"),
    json_output: bool = typer.Option(False, "--json", help="Zwróć wynik w formacie JSON")
):
    """
    Skanuje repozytoria wskazanego celu i raportuje naruszenia polityki.
    Wymaga ustawienia zmiennej środowiskowej GITHUB_TOKEN.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("devops_toolkit.services.github_service").setLevel(logging.DEBUG)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        typer.secho("Błąd: Brak zmiennej środowiskowej GITHUB_TOKEN. Nigdy nie podawaj tokena jako flagi w CLI!", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    has_errors, results = audit_target(target, token, is_org)

    if json_output:
        typer.echo(json.dumps({
            "target": target,
            "has_errors": has_errors,
            "issues": results
        }))
        sys.exit(1 if has_errors else 0)

    for msg in results:
        typer.echo(msg)

    if has_errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    app()