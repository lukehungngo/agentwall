"""AgentWall CLI."""

from __future__ import annotations

from pathlib import Path

import typer

from agentwall.models import ScanConfig, Severity
from agentwall.reporters.json_reporter import JsonReporter
from agentwall.reporters.terminal import TerminalReporter
from agentwall.scanner import scan as run_scan

app = typer.Typer(
    name="agentwall",
    help="Memory security scanner for AI agents.",
    add_completion=False,
    no_args_is_help=True,
)


@app.callback()
def _root() -> None:
    pass

_SEVERITY_MAP: dict[str, Severity | None] = {
    "critical": Severity.CRITICAL,
    "high": Severity.HIGH,
    "medium": Severity.MEDIUM,
    "low": Severity.LOW,
    "none": None,
}

_SEVERITY_RANK: dict[Severity, int] = {
    Severity.CRITICAL: 0,
    Severity.HIGH: 1,
    Severity.MEDIUM: 2,
    Severity.LOW: 3,
    Severity.INFO: 4,
}

_STATIC_LAYERS = {"L0", "L1", "L2", "L3", "L4", "L5", "L6"}
# L7 (--dynamic) and L8 (--llm-assist) are opt-in via flags, not --layers


@app.command()
def scan(
    path: Path = typer.Argument(..., help="Target directory to scan."),  # noqa: B008
    framework: str | None = typer.Option(None, "--framework", "-f", help="Force framework."),  # noqa: B008
    output: Path | None = typer.Option(None, "--output", "-o", help="JSON output file."),  # noqa: B008
    fail_on: str = typer.Option("high", "--fail-on", help="Severity threshold: critical|high|medium|low|none"),  # noqa: B008
    layers: str | None = typer.Option(None, "--layers", help="Comma-separated layers to run (e.g. L0,L1,L2). Default: all static."),  # noqa: B008
    dynamic: bool = typer.Option(False, "--dynamic", help="Enable L7 runtime instrumentation."),  # noqa: B008
    llm_assist: bool = typer.Option(False, "--llm-assist", help="Enable L8 LLM confidence scoring."),  # noqa: B008
    fast: bool = typer.Option(False, "--fast", help="Fast mode: L0-L2 only."),  # noqa: B008
) -> None:
    """Scan an agent directory for memory and tool security issues."""
    if not path.exists():
        typer.echo(f"Error: path does not exist: {path}", err=True)
        raise typer.Exit(2)

    if fail_on not in _SEVERITY_MAP:
        typer.echo(f"Error: --fail-on must be one of {list(_SEVERITY_MAP)}", err=True)
        raise typer.Exit(2)

    # Build scan config
    if fast:
        config = ScanConfig.fast()
    elif layers:
        layer_set = {part.strip().upper() for part in layers.split(",")}
        invalid = layer_set - _STATIC_LAYERS
        if invalid:
            typer.echo(f"Error: unknown layers: {invalid}. Valid: {_STATIC_LAYERS}", err=True)
            raise typer.Exit(2)
        config = ScanConfig(layers=layer_set)
    else:
        config = ScanConfig.default()

    config.dynamic = dynamic
    config.llm_assist = llm_assist

    result = run_scan(target=path, framework=framework, config=config)

    if result.errors and not result.findings:
        typer.echo(f"Scan error: {result.errors[0]}", err=True)
        raise typer.Exit(2)

    TerminalReporter().render(result)

    if output is not None:
        JsonReporter().render(result, output)
        typer.echo(f"JSON report written to {output}")

    threshold = _SEVERITY_MAP[fail_on]
    if threshold is None:
        raise typer.Exit(0)

    threshold_rank = _SEVERITY_RANK[threshold]
    triggered = any(
        _SEVERITY_RANK[f.severity] <= threshold_rank for f in result.findings
    )
    raise typer.Exit(1 if triggered else 0)


@app.command()
def version() -> None:
    """Show AgentWall version."""
    from agentwall import __version__

    typer.echo(f"AgentWall v{__version__}")
