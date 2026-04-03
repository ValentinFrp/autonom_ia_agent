import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.spinner import Spinner
from rich import print as rprint
from agent.core import run_agent
from models.task import TaskStatus

console = Console()


def display_result(result) -> None:
    status_color = "green" if result.status == TaskStatus.COMPLETED else "red"
    status_label = result.status.value.upper()

    console.print()
    console.print(Panel(
        result.summary,
        title="[bold cyan]Rapport final[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))

    table = Table(title="Outils utilisés", border_style="dim", show_lines=True)
    table.add_column("Etape", style="bold", justify="center", width=6)
    table.add_column("Outil", style="magenta", width=16)
    table.add_column("Inputs", style="yellow")
    table.add_column("Aperçu résultat", style="dim")

    for i, tc in enumerate(result.tool_calls, start=1):
        inputs_str = ", ".join(f"{k}={v}" for k, v in tc.inputs.items())
        output_preview = tc.output[:80].replace("\n", " ") + ("..." if len(tc.output) > 80 else "")
        table.add_row(str(i), tc.name, inputs_str, output_preview)

    if result.tool_calls:
        console.print(table)

    console.print()
    console.print(
        f"  Statut : [{status_color}]{status_label}[/{status_color}]  |  "
        f"Iterations : [bold]{result.iterations}[/bold]"
    )
    console.print()


def main() -> None:
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        console.print(Panel(
            "[bold cyan]Agent IA Autonome[/bold cyan]\n"
            "[dim]Exemples : 'analyse le site https://example.com' "
            "ou 'résume les concurrents de Notion'[/dim]",
            border_style="cyan",
        ))
        console.print()
        task = console.input("[bold]Tâche >[/bold] ").strip()

    if not task:
        console.print("[red]Aucune tâche fournie.[/red]")
        sys.exit(1)

    console.print()
    with console.status(f"[cyan]Agent en cours d'exécution...[/cyan]", spinner="dots"):
        result = run_agent(task)

    display_result(result)


if __name__ == "__main__":
    main()
