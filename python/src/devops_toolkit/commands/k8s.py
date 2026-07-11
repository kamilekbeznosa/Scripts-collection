import typer
import sys
import json
from devops_toolkit.services.k8s_service import check_cluster_health

app = typer.Typer(help="Diagnostyka klastra K8s.")


@app.command()
def check(
    namespace: str = typer.Option("default", "--namespace", "-n"),
    json_output: bool = typer.Option(False, "--json", help="Zwróć wynik w formacie JSON"),
):
    has_critical = check_cluster_health(namespace)

    if json_output:
        typer.echo(json.dumps({"namespace": namespace, "has_critical_errors": has_critical}))
        sys.exit(1 if has_critical else 0)

    if has_critical:
        typer.secho("Wykryto błędy!", fg=typer.colors.RED)
        sys.exit(1)
    else:
        typer.secho("Klaster OK.", fg=typer.colors.GREEN)
        sys.exit(0)


if __name__ == "__main__":
    app()
