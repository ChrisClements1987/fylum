"""
History and manifest endpoints
"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from datetime import datetime
from src.api.models.responses import HistoryResponse, HistoryEntry

router = APIRouter()


@router.get("/", response_model=HistoryResponse)
async def get_history():
    """Get operation history from manifest"""
    try:
        manifest_path = Path("_fylum_index.json")
        
        if not manifest_path.exists():
            return HistoryResponse(entries=[], total=0)
        
        with open(manifest_path, "r") as f:
            manifest_data = json.load(f)
        
        entries = []
        for run in manifest_data:
            entries.append(
                HistoryEntry(
                    timestamp=datetime.fromisoformat(run["timestamp"]),
                    operation="clean",
                    files_affected=len(run["actions"]),
                    details={"actions": len(run["actions"])}
                )
            )
        
        return HistoryResponse(
            entries=entries,
            total=len(entries)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest")
async def get_latest_run():
    """Get details of the most recent operation"""
    try:
        manifest_path = Path("_fylum_index.json")
        
        if not manifest_path.exists():
            return {"message": "No history available"}
        
        with open(manifest_path, "r") as f:
            manifest_data = json.load(f)
        
        if not manifest_data:
            return {"message": "No history available"}
        
        latest = manifest_data[-1]
        return {
            "timestamp": latest["timestamp"],
            "files_processed": len(latest["actions"]),
            "actions": latest["actions"][:10]  # Return first 10 actions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
