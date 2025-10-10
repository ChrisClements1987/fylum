"""
File operation endpoints
"""

from fastapi import APIRouter, HTTPException
from src import config
from src.engine import RuleEngine
from src.processor import FileProcessor
from src.undo import UndoManager
from src.api.models.responses import ScanResponse, CleanResponse, UndoResponse, FileAction

router = APIRouter()


@router.post("/scan", response_model=ScanResponse)
async def scan_directories():
    """Scan directories and return pending operations (dry run)"""
    try:
        cfg = config.load_config()
        engine = RuleEngine(config=cfg, dry_run=True)
        actions = engine.process_directories()
        
        file_actions = [
            FileAction(
                source=str(src),
                destination=str(dst),
                action_type="move"
            )
            for src, dst in actions
        ]
        
        return ScanResponse(
            actions=file_actions,
            total_files=len(file_actions),
            message=f"Found {len(file_actions)} file(s) to process"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clean", response_model=CleanResponse)
async def clean_directories():
    """Execute file organization"""
    try:
        cfg = config.load_config()
        engine = RuleEngine(config=cfg, dry_run=False)
        actions = engine.process_directories()
        
        if not actions:
            return CleanResponse(
                processed=0,
                success=True,
                message="No files found to process"
            )
        
        processor = FileProcessor(rename_format=cfg.rename_format, dry_run=False)
        processed = processor.process_actions(actions)
        
        return CleanResponse(
            processed=processed,
            success=True,
            message=f"Successfully processed {processed} file(s)",
            manifest_path="_fylum_index.md"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/undo", response_model=UndoResponse)
async def undo_last_operation():
    """Undo the last file organization operation"""
    try:
        undo_manager = UndoManager()
        reverted = undo_manager.revert_last_run()
        
        if reverted > 0:
            return UndoResponse(
                reverted=reverted,
                success=True,
                message=f"Successfully reverted {reverted} file(s)"
            )
        else:
            return UndoResponse(
                reverted=0,
                success=False,
                message="No previous operation found to undo"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
