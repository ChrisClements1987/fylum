
import typer
from typing_extensions import Annotated

from src import config
from src.engine import RuleEngine
from src.processor import FileProcessor
from src.undo import UndoManager

app = typer.Typer()

@app.command()
def clean(
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Preview the file operations without making any changes."
        ),
    ] = False
):
    """Organizes files in the target directories based on the rules in config.yaml."""
    cfg = config.load_config()
    typer.echo("Configuration loaded successfully.")
    
    if dry_run:
        typer.echo("--- DRY RUN MODE ---")
        typer.echo("No files will be moved or renamed.")

    # Instantiate and run the engine
    engine = RuleEngine(config=cfg, dry_run=dry_run)
    actions = engine.process_directories()

    if not actions:
        typer.echo("No files found that match the rules. Everything is already organized.")
        raise typer.Exit()

    typer.echo(f"Found {len(actions)} actions to perform.")

    processor = FileProcessor(rename_format=cfg.rename_format, dry_run=dry_run)
    processed = processor.process_actions(actions)

    if dry_run:
        typer.echo(f"\n[DRY RUN] Would have processed {processed} files.")
    else:
        typer.echo(f"\nSuccessfully processed {processed} files.")
        typer.echo("Index manifest updated: _fylum_index.md")
    
    typer.echo("Done.")

@app.command()
def undo():
    """Reverts the last cleaning operation."""
    typer.echo("Looking for the index manifest to undo the last operation...")
    
    undo_manager = UndoManager()
    reverted_count = undo_manager.revert_last_run()
    
    if reverted_count > 0:
        typer.echo(f"Successfully reverted {reverted_count} files to their original locations.")
    else:
        typer.echo("No files were reverted.")


@app.callback()
def main():
    """
    Fylum: A smart file organizer.
    """
    pass

if __name__ == "__main__":
    app()

