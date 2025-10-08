
from pathlib import Path
from typing import List, Tuple

from src.config import Config

class RuleEngine:
    def __init__(self, config: Config, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run

    def process_directories(self) -> List[Tuple[Path, Path]]:
        """Scans target directories and applies rules to find files to move."""
        actions = []
        for target_dir_str in self.config.target_directories:
            target_dir = Path(target_dir_str).expanduser()
            if not target_dir.is_dir():
                print(f"Warning: Target directory '{target_dir}' does not exist or is not a directory.")
                continue

            for file_path in target_dir.rglob('*'):
                if not file_path.is_file():
                    continue

                # Check against ignore patterns
                if any(file_path.match(pattern) for pattern in self.config.ignore_patterns):
                    continue

                # Check against rules
                for rule in self.config.rules:
                    if file_path.suffix.lower() in rule.extensions:
                        destination_dir = Path(rule.destination).expanduser()
                        destination_path = destination_dir / file_path.name
                        actions.append((file_path, destination_path))
                        break # Move to next file once a rule has matched
        return actions

