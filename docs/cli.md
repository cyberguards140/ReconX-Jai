# CLI Architecture

The ReconX command-line interface leverages Typer for command structures and Rich for high-fidelity console visuals.

## Design

The CLI operates purely as a thin presentation layer, routing all actions directly to the `src/reconx/services/` layer. It does **not** load the `WorkflowEngine` or `PluginManager` natively in its commands.

## Visual Experience

### Tables
Operations like `reconx workflow list` and `reconx plugin list` use `rich.table.Table` with colored columns (e.g. `magenta` headers and `cyan` property names).

### Progress Bars
Execution commands (`reconx workflow run`) trigger an asynchronous `rich.progress.Progress` spinner indicating that the underlying service is orchestrating the scan.

### Consistent Colors
- Success states: `[bold green]`
- Errors: `[bold red]`
- Properties/IDs: `[cyan]`
