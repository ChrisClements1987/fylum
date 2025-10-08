
from pathlib import Path
import json
import shutil
from typing import Optional, Dict, List


class UndoManager:
    def __init__(self):
        self.json_manifest_path = Path("_fylum_index.json")

    def get_last_run(self) -> Optional[Dict]:
        if not self.json_manifest_path.exists():
            return None
        
        try:
            with open(self.json_manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
            
            if not manifest_data:
                return None
            
            return manifest_data[-1]
        except (json.JSONDecodeError, IOError):
            return None

    def revert_last_run(self) -> int:
        last_run = self.get_last_run()
        
        if not last_run:
            print("No previous run found to undo.")
            return 0
        
        actions = last_run.get("actions", [])
        reverted_count = 0
        
        for action in reversed(actions):
            source = Path(action["source"])
            destination = Path(action["destination"])
            
            if not destination.exists():
                print(f"Warning: File not found at {destination}, skipping...")
                continue
            
            try:
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(source))
                print(f"Reverted: {destination} -> {source}")
                reverted_count += 1
            except Exception as e:
                print(f"Error reverting {destination}: {e}")
        
        self._remove_last_run()
        
        return reverted_count

    def _remove_last_run(self) -> None:
        try:
            with open(self.json_manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
            
            if manifest_data:
                manifest_data.pop()
            
            with open(self.json_manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not update manifest: {e}")
