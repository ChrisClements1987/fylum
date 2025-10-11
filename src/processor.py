
from pathlib import Path
from typing import List, Tuple
from datetime import datetime
import shutil
import json


class FileAction:
    def __init__(self, source: Path, destination: Path):
        self.source = source
        self.destination = destination
        self.timestamp = datetime.now()


class FileProcessor:
    def __init__(self, rename_format: str, dry_run: bool = False, notification_manager=None):
        self.rename_format = rename_format
        self.dry_run = dry_run
        self.manifest_path = Path("_fylum_index.md")
        self.actions_log = []
        self.notification_manager = notification_manager

    def apply_rename_format(self, file_path: Path) -> str:
        modification_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        original_stem = file_path.stem
        extension = file_path.suffix
        
        new_name = self.rename_format.format(
            date=modification_time,
            original_filename=original_stem
        )
        
        return f"{new_name}{extension}"

    def process_actions(self, actions: List[Tuple[Path, Path]]) -> int:
        processed_count = 0
        
        for source, destination_dir_path in actions:
            renamed_filename = self.apply_rename_format(source)
            final_destination = destination_dir_path.parent / renamed_filename
            
            if self.dry_run:
                print(f"[DRY RUN] Would move: {source} -> {final_destination}")
                self.actions_log.append(FileAction(source, final_destination))
                processed_count += 1
            else:
                try:
                    final_destination.parent.mkdir(parents=True, exist_ok=True)
                    
                    if final_destination.exists():
                        counter = 1
                        while final_destination.exists():
                            new_name = f"{final_destination.stem}_{counter}{final_destination.suffix}"
                            final_destination = final_destination.parent / new_name
                            counter += 1
                    
                    shutil.move(str(source), str(final_destination))
                    print(f"Moved: {source} -> {final_destination}")
                    self.actions_log.append(FileAction(source, final_destination))
                    processed_count += 1
                    
                except Exception as e:
                    print(f"Error moving {source}: {e}")
        
        if not self.dry_run and self.actions_log:
            self._write_manifest()
            
            # Send success notification
            if self.notification_manager and processed_count > 0:
                from src.notifications.manager import NotificationType
                self.notification_manager.send_notification(
                    title="Files Organized",
                    message=f"Successfully processed {processed_count} file(s)",
                    notification_type=NotificationType.SUCCESS
                )
        
        return processed_count

    def _write_manifest(self) -> None:
        with open(self.manifest_path, "a", encoding="utf-8") as f:
            f.write(f"\n## Fylum Run - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("| Original Path | New Path |\n")
            f.write("|---------------|----------|\n")
            
            for action in self.actions_log:
                f.write(f"| {action.source} | {action.destination} |\n")
            
            f.write("\n")
        
        json_manifest_path = Path("_fylum_index.json")
        manifest_data = []
        if json_manifest_path.exists():
            with open(json_manifest_path, "r", encoding="utf-8") as f:
                try:
                    manifest_data = json.load(f)
                except json.JSONDecodeError:
                    manifest_data = []
        
        run_data = {
            "timestamp": datetime.now().isoformat(),
            "actions": [
                {
                    "source": str(action.source),
                    "destination": str(action.destination)
                }
                for action in self.actions_log
            ]
        }
        manifest_data.append(run_data)
        
        with open(json_manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)
