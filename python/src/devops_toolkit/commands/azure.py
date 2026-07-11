import typer
import requests
import sys
import json
from devops_toolkit.services.azure_service import get_azure_costs

app = typer.Typer(help="Narzędzie do raportowania kosztów Azure.")


@app.command()
def report(
    sub_id: str = typer.Option(..., "--subscription-id", envvar="AZURE_SUBSCRIPTION_ID"),
    webhook: str = typer.Option(..., "--webhook", envvar="WEBHOOK_URL"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    json_output: bool = typer.Option(False, "--json", help="Zwróć wynik w formacie JSON"),
):
    data = get_azure_costs(sub_id, is_dry_run=dry_run)

    if json_output:
        typer.echo(json.dumps({"status": "success", "report": data}))
        sys.exit(0)

    if dry_run:
        typer.secho(f"[DRY-RUN] Wygenerowano dane:\n{data}", fg=typer.colors.YELLOW)
    else:
        typer.echo("Wysyłanie na webhook...")
        try:
            requests.post(webhook, json={"text": data}, timeout=10).raise_for_status()
            typer.secho("Wysłano!", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"Błąd: {e}", fg=typer.colors.RED)
            sys.exit(3)


if __name__ == "__main__":
    app()
